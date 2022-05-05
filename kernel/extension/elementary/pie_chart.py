import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from extension.util import format_figure
from gamma.dispatch import DICT
from gamma.result_card import ResultCard

FONT_SIZE = 32


def not_integer_nor_too_big(components: DICT) -> bool:
    num = components['input_evaluated']
    return int(num) != num and 0 < num < 10000


def plot_pie_chart(components: DICT, parameters=None) -> tuple[Figure, str]:
    num = components['input_evaluated']
    n = int(num)
    frac = num - n
    if n == 0:
        fig = plt.figure(figsize=(1, 1))
        axe_frac = fig.add_axes([0, 0, 1, 1])
    else:
        fig = plt.figure(figsize=(5, 2))
        axe_plus = fig.add_axes([0.5, 0.5, 1, 1])
        axe_plus.text(0, 0, '+', ha='center', va='center').set_fontsize(FONT_SIZE)
        axe_plus.axis('off')
        axe_int = fig.add_axes([-0.25, 0, 1, 1])
        axe_int.pie([1])
        axe_int.text(0, 0, f'×{n}' if n > 1 else '', color='white', ha='center', va='center').set_fontsize(FONT_SIZE)
        axe_frac = fig.add_axes([0.25, 0, 1, 1])
    axe_frac.pie([frac, 1-frac])
    return fig, 'pie_chart'


pie_chart_card = ResultCard('Pie chart', None, eval_method=plot_pie_chart, format_output=format_figure,
                            applicable=not_integer_nor_too_big)
