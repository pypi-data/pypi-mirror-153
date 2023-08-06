from matplotlib import pyplot as plt


def lineplot(dataframe):
    """This is a small example of visualizing data. You can build your own visualization method referring to this method.

    .. code-block:: python

        df = task.passive...(
            ...
        ).DataFrame
        lineplot(df)
        plt.legend()

    Args:
        dataframe (DataFrame): pandas DataFrame.

    Returns:
        None
    """
    for c in dataframe.columns:
        plt.plot(dataframe[c], label=c)
