from typing import cast

import cplot
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sympy import Expr, Symbol, lambdify

from extension.util import DICT, format_figure, no_undefined_function
from gamma.result_card import ResultCard


def plot_complex(components: DICT, parameters=None) -> tuple[Figure, str]:
    func: Expr = components['input_evaluated']
    z: Symbol = list(cast(set[Symbol], func.free_symbols))[0]
    cplot.plot(lambdify(z, func, 'numpy'), (-10, 10, 200), (-10, 10, 200))
    return plt.gcf(), 'plot_3d'


plot_complex_card = ResultCard('Complex Plot', None, eval_method=plot_complex, format_output=format_figure,
                               applicable=no_undefined_function)
