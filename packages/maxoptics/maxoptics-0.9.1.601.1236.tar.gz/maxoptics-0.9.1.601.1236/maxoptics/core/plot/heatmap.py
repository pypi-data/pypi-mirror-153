import matplotlib.pyplot as plt
import numpy as np


def heatmap(x, y, Z):
    """This is a small example of visualizing data. You can build your own visualization method referring to this method.
    .. code-block:: python

        x, y, Z = data.raw_data["horizontal"], data.raw_data["vertical"], data.raw_data["data"]
        fig, ax = heatmap(x, y, Z)

    Args:
        x (list[float]): 1-D array.
        y (list[float]): 1-D array.
        Z (list[list[float]]): 2-D array.

    Returns:
        fig, ax
    """
    if len(x) == 1:
        x = [x[0] - 0.001, x[0] + 0.001]
    elif len(x) == len(Z[0]):
        x = [x[0] - (x[1] - x[0])] + x

    if len(y) == 1:
        y = [y[0] - 0.001, y[0] + 0.001]
    elif len(y) == len(Z):
        y = [y[0] - (y[1] - y[0])] + y

    X, Y = np.meshgrid(x, y)
    fig, ax = plt.subplots()
    pmesh = ax.pcolormesh(X, Y, Z, cmap="jet")
    plt.colorbar(pmesh, ax=ax)

    return fig, ax
