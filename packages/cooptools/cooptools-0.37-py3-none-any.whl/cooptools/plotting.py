from typing import List, Tuple

def plot_series(points: List[Tuple[int, float]],
                 ax,
                 color=None,
                 type=None,
                 label=None,
                 line_width: int = None,
                 line_style: str = None,
                 point_size = None):
    """

    :param points:
    :param ax:
    :param color:
    :param type:
    :param label:
    :param line_width:
    :param line_style: [‘solid’, ‘dashed’, ‘dashdot’, ‘dotted’, (offset, on-off-dash-seq), '-', '--', '-.', ':', 'None', ' ', '']
    :return:
    """

    if points is None or len(points) == 0:
        return

    res = list(zip(*points))

    if type is None:
        ax.plot(res[0], res[1], color=color, linewidth=line_width, label=label, linestyle=line_style)
    elif type == 'scatter':
        ax.scatter(res[0], res[1], color=color, label=label, s=point_size)