import getpass

from maxoptics.core.logger import (
    error_print,
    info_print,
    success_print,
    warn_print,
)
from .HttpIO import HttpIO


class BaseClient(HttpIO):
    def __init__(self, url_key) -> None:
        super().__init__(url_key)

    @property
    def token(self):
        ret = self.config.Token
        if ret == "":
            error_print(
                "Error occurs when fetching token: Token is not initialized.\n"
                "This may caused by:\n"
                "1. You directly initialized a MaxOptics(Client) Instance (You should use MosLibrary).\n"
                "2. You directly initialized a WhaleClients(ResultHandler) Instance (You should use "
                "run_`simu_name` to get corresponding instance).\n"
                "3. The token was explicitly replaced.\n"
                "\n"
                "If you really want to do (1, 2), please:\n"
                "1. For MaxOptics, call login().\n"
                "2. For WhaleClinet, Pass the `config` of your previous created MaxOptics(Client) as the 3rd "
                "parameter\n"
            )
        return ret

    def ping(self):
        """ """
        params = {}

        info_print(
            "Connecting to Server  %s" % self.config.ServerHost, end=" "
        )
        result = self.post(**params)
        if result["success"] is False:
            error_print("Connection Failed, %s" % result["result"]["msg"])
            exit(0)
        else:
            success_print("Succeed.")
            return True

    def login(self):
        """ """
        info_print("Connecting to ", self.api_url)
        if self.config.DefaultUser:
            username = self.config.DefaultUser
        else:
            username = input("MaxOptics Studio Username:")
        if self.config.DefaultPassword:
            passwd = self.config.DefaultPassword
        else:
            passwd = getpass.getpass("Password:")

        params = {
            "name": username,
            "password": passwd,
        }

        result = self.post(**params)
        if result["success"] is False:
            warn_print("Login failed, %s" % result["result"]["msg"])
            raise ConnectionRefusedError("Connection Failed")
        else:
            self.config = self.config.update(Token=result["result"]["token"])

            info_print(username, " ", end=" ")
            success_print("Login Success.")
            info_print("Welcome to use MaxOptics Studio SDK")
            self.__get_user()

    def __get_user(self):
        result = self.post(url="get_user", token=self.token)
        if result["success"] is False:
            raise ConnectionRefusedError("Connection Failed")
        else:
            self.user_id = result["result"]["id"]

    # @atexit.register(self)
    def logout(self):
        if self.token:
            params = {"token": self.token}
            self.post(**params)
            info_print("Logout successfully.")
        else:
            warn_print("You haven't login yet")
