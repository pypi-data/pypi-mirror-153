import matplotlib.pyplot as plt

from maxoptics.core.plot.PolygonLike import compromised_transform


def draw_polygon(project, xysize=[20, 20], facecolor=None):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim((-xysize[0], xysize[0]))
    ax.set_ylim((-xysize[1], xysize[1]))

    for _ in project.__dict__["polygons"]:
        item = compromised_transform(_)
        ax.add_patch(item.__plot__(facecolor))
    plt.show()
