import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from sympy import Expr, lambdify

from extension.util import DICT, format_figure, no_undefined_function, sorted_free_symbols
from gamma.result_card import ResultCard


def plot_contour(components: DICT, parameters=None) -> tuple[Figure, str]:
    func: Expr = components['input_evaluated']
    x, y = sorted_free_symbols(func)
    z = lambdify((x, y), func, 'numpy')
    X, Y = np.meshgrid(np.arange(-10, 10, 0.1), np.arange(-10, 10, 0.1))
    Z = z(X, Y)
    fig, axe = plt.subplots()
    cset = axe.contourf(X, Y, Z)
    axe.clabel(axe.contour(X, Y, Z, cset.levels, colors='k'))
    axe.set(xlabel=x.name, ylabel=y.name)
    return fig, 'plot_contour'


plot_contour_card = ResultCard('Contour Plot', None, eval_method=plot_contour, format_output=format_figure,
                               applicable=no_undefined_function)
