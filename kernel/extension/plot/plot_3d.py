from matplotlib.figure import Figure
from sympy import Expr
from sympy.plotting.plot import plot3d

from extension.util import DICT, format_figure, no_undefined_function, sorted_free_symbols
from gamma.result_card import ResultCard


def plot_3d(components: DICT, parameters=None) -> tuple[Figure, str]:
    func: Expr = components['input_evaluated']
    x, y = sorted_free_symbols(func)
    sympy_plot = plot3d(func, (x, -10, 10), (y, -10, 10))
    return sympy_plot._backend.fig, 'plot_3d'  # type: ignore


plot_3d_card = ResultCard('3D Plot', None, eval_method=plot_3d, format_output=format_figure,
                          applicable=no_undefined_function)
