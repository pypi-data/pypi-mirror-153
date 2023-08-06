import inspect
import json
import re
import traceback

import requests

import maxoptics.core.utils
from maxoptics.config import Config
from maxoptics.core.error import (
    ConnectTimeoutError,
    MaxRetryError,
    NewConnectionError,
    PostResultFailedError,
)
from maxoptics.core.logger import debug_pprint, debug_print, error_print
from maxoptics.core.utils import fstr


class HttpIO:
    def __init__(self, url_key) -> None:
        super().__init__()
        self.thread_status = None
        self.url_key = url_key
        self.__config = Config.update()

    @property
    def api_url(self):
        return get_valid_api(self.url_key, self)

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, dikt):
        if isinstance(dikt, dict):
            dikt = dikt
        elif hasattr(dikt, "asdict"):
            dikt = dikt.asdict()

        self.__config = Config.update(**dikt)

    def post(self, url="", __base_params__={}, json_params="", **kwargs):
        try:
            kwargs.update(__base_params__)
            if url:
                this_url = self.api_url % url
            else:
                this_url = self.api_url % (inspect.stack()[1][3])

            debug_print(this_url)
            debug_print(json_params or json.dumps(kwargs))

            r = requests.post(
                this_url,
                data=json_params or json.dumps(kwargs),
                headers={
                    "Content-Type": "application/json",
                    "Connection": "close",
                },
            )

            if r.status_code == 404:
                raise PostResultFailedError()
            self.thread_status = False
            return json.loads(r.text)
        except PostResultFailedError:
            error_print("Failed")
            error_print("Server %s API Doesn't Exist" % this_url)
            self.thread_status = False
            return json.loads(
                '{"success": false, "result": {"code": 501, "msg": "Server Failed"}}'
            )
        except (NewConnectionError, MaxRetryError, ConnectTimeoutError):
            error_print("Server %s May " % this_url)
            error_print("Failed")
            self.thread_status = False
            return json.loads(
                '{"success": false, "result": {"code": 501, "msg": "Server Failed"}}'
            )
        except requests.exceptions.ConnectionError:
            error_print("Failed")
            self.thread_status = False
            error_print(
                "Cannot connect Server %s, please retry later" % self.api_url
            )
            return json.loads(
                '{"success": false, "result": {"code": 502, "msg": "Server Failed"}}'
            )
        except requests.exceptions.ChunkedEncodingError:
            error_print("Failed")
            error_print("ChunkedEncodingError -- Retry later")
            self.thread_status = False
            return json.loads(
                '{"success": false, "result": {"code": 503, "msg": "Server Error"}}'
            )
        except json.JSONDecodeError:
            error_print(f"{inspect.stack()[1][3]} Failed")
            error_print("Unfortunately -- Retry later")
            error_print(
                "Failed to load response as JSON. Because response is:\n"
            )
            error_print(r.text)
        except Exception as e:
            debug_print(
                f"{url = } token %s" % (kwargs.get("token")), "\nurl", url
            )
            debug_pprint({**__base_params__, **kwargs})
            debug_pprint(r.text)

            error_print(f"{this_url} Failed")
            error_print("Unfortunately -- Retry later", e)
            traceback.print_exc()
            self.thread_status = False
            return json.loads(
                '{"success": false, "result": {"code": 509, "msg": "Server Error"}}'
            )


def get_valid_api(url_key, ioc: HttpIO):
    url_template: str = getattr(ioc.config, url_key)
    try:
        url_template.format(**ioc.config.__dict__)

    except KeyError as e:
        if "ServerHost" in e.args:
            api_address = input("Server:\n").strip()
            port = 80
            while True:
                api_address = input("Server:\n").strip()
                if re.match(
                    r"^http(s)?://([A-Za-z0-9-]+[./])+[A-Za-z0-9]+(/)?$",
                    api_address,
                ):
                    assert len(api_address) > 1
                    api_address = fstr(api_address)
                    api_address = maxoptics.core.utils.removesuffix("/")
                    api_address = api_address.__str__
                    break

                elif re.match(
                    r"^([A-Za-z0-9-]+[./])+[A-Za-z0-9]+$", api_address
                ):
                    if ":" in api_address and api_address.count(":") == 1:
                        api_address, port = api_address.split(":")
                    break

            ioc.config = Config.update(ServerHost=api_address, ServerPort=port)

        else:
            raise e

    api_url = url_template.format(**ioc.config.__dict__)
    return api_url
