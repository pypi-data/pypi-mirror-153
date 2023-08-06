"""The TaskFile module provides a result container for task return."""
import numpy as np
import pandas as pd

from maxoptics.core.component.base.base import FP
from maxoptics.core.error import InvalidInputError


class TaskFile(FP):
    """The TaskFile class is a container class for task result.
    Base on target of result, a TaskFile instance will read corresponding data
    in raw result to sum up a pandas.DataFrame.

    For heatmap/intensity type result, using "horizontal" and "vertical" from `raw_data` is a better choice,
    because DataFrame's columns and index are the deltas, not suitable for drawing grid.
    """

    def __init__(self, data, task, *args, **kwargs):
        self.task_id = task.task_id
        self.task = task
        self.raw_data = data
        self.args = args
        self.kwargs = kwargs
        self.data_type = str(kwargs.get("target") or args[0])
        for thing in data:
            setattr(self, thing, data[thing])

        if "table" in self.data_type.lower():
            self.columns = self.raw_data.get("header") or self.raw_data.get(
                "columns"
            )
            self.index = self.raw_data.get("index")
            self.index_label = self.raw_data.get("index_label") or None

        elif "line" in self.data_type.lower():
            self.data = np.transpose(self.raw_data["data"])
            legends = (
                self.raw_data.get("legend")
                or self.raw_data.get("columns")
                or ["data"]
            )
            self.columns = legends
            self.index = self.raw_data.get("horizontal") or self.raw_data.get(
                "index"
            )
            self.index_label = self.raw_data.get("index_label") or None

        elif "intensity" in self.data_type.lower():
            self.columns = self.raw_data.get("dWidth") or self.raw_data.get(
                "columns"
            )
            self.index = self.raw_data.get("dHeight") or self.raw_data.get(
                "index"
            )
            self.index_label = self.raw_data.get("index_label") or None

        else:
            print("Invalid target type!")
            print(self.data_type)
            raise InvalidInputError

    @property
    def DataFrame(self):
        """Sum up a DataFrame."""
        df = pd.DataFrame().from_records(data=self.data, columns=self.columns)
        if self.index:
            df.index = self.index
        return df

    # TODO: def __enter__(self):

    # TODO: def __exit__(self):

    # TODO: def __del__(self):
