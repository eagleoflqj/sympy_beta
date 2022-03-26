import enum
import itertools
import sys
from typing import Any, Callable

import docutils.core
import sympy
from sympy.core.symbol import Symbol

import gamma.diffsteps
import gamma.intsteps
from api.data_type import Document, FactorDiagram, List, Plot, Reference, Table, TruthTable
from extension.elementary.binary_form import binary_form_card
from extension.elementary.chinese_numeral import chinese_numeral_card
from extension.elementary.roman_numeral import roman_numeral_card
from extension.ntheory.is_prime import is_prime_card
from extension.ntheory.modulo import modulo_card
from extension.ntheory.totient import totient_card
from gamma.evaluator import eval_node
from gamma.result_card import MultiResultCard, ResultCard

# Formatting functions
_function_formatters = {}


def formats_function(name):
    def _formats_function(func):
        _function_formatters[name] = func
        return func
    return _formats_function


@formats_function('diophantine')
def format_diophantine(result, node, formatter):
    variables = sorted(str(s) for s in eval_node(node.args[0]).atoms(sympy.Symbol))
    if isinstance(result, set):
        return format_nested_list_title(*variables)(result, formatter)
    else:
        return format_nested_list_title(*variables)([result], formatter)


def format_by_type(result, function_name, node, formatter):
    """
    Format something based on its type and on the input to Gamma.
    """
    if function_name in _function_formatters:
        return _function_formatters[function_name](result, node, formatter)
    elif function_name in all_cards and all_cards[function_name].format_output:
        return all_cards[function_name].format_output(result, formatter)
    elif isinstance(result, (list, tuple)):
        return format_list(result, formatter)
    else:
        return formatter(result)


def format_document(arg: str, formatter):
    return Document(html=arg)


def format_steps(arg, formatter):
    arg['type'] = 'StepContainer'
    return arg


def format_long_integer(line, integer, variable):
    intstr = str(integer)
    if len(intstr) > 100:
        # \xe2 is Unicode ellipsis
        return intstr[:20] + "..." + intstr[len(intstr) - 21:]
    return line % intstr


def format_integral(line, result, components):
    if components['limits']:
        limits = ', '.join(map(repr, components['limits']))
    else:
        limits = ', '.join(map(repr, components['variables']))

    return line.format(_var=limits) % components['integrand']


def format_dict_title(*title: str):
    def _format_dict(dictionary, formatter):
        data = Table(titles=title, rows=[])
        try:
            fdict = dictionary.items()
            if not any(isinstance(i, Symbol) for i in dictionary):
                fdict = sorted(fdict)
            for key, val in fdict:
                data['rows'].append([str(key), str(val)])
            return data
        except AttributeError:  # not iterable/not a dict
            return formatter(dictionary)
    return _format_dict


def format_list(items, formatter):
    try:
        return List(list=[formatter(item) for item in items])
    except TypeError:  # not iterable, like None
        return formatter(items)


def format_nested_list_title(*titles: str):
    def _format_nested_list_title(items, formatter):
        try:
            return Table(titles=titles, rows=[[formatter(sub_item) for sub_item in item] for item in items])
        except TypeError:  # not iterable, like None
            return formatter(items)
    return _format_nested_list_title


def format_series_fake_title(title, evaluated):
    if len(evaluated.args) >= 3:
        about = evaluated.args[2]
    else:
        about = 0
    if len(evaluated.args) >= 4:
        up_to = evaluated.args[3]
    else:
        up_to = 6
    return title.format(about, up_to)


def format_truth_table(table, formatter):
    # table is (variables, [(bool, bool...)] representing combination of values
    # and result
    return TruthTable(titles=[str(s) for s in table[0]] + ["Values"],
                      rows=[[str(v) for v in entry] for entry in table[1]])


def format_approximator(approximation, formatter):
    obj, digits = approximation
    return formatter(obj, digits=digits)


def format_factorization_diagram(factors, formatter):
    primes = []
    for prime in reversed(sorted(factors)):
        times = factors[prime]
        primes.extend([prime] * times)
    return FactorDiagram(primes=primes)


def format_plot(plot_data: tuple[str, list[dict]], formatter):
    return Plot(variable=plot_data[0], graphs=plot_data[1])


def format_plot_input(result_statement, input_repr, components):
    if 'input_evaluated' in components:
        functions = components['input_evaluated']
        if isinstance(functions, list):
            return [str(f) for f in functions]
        if isinstance(functions, dict):
            return [f'{y} = {x}' for y, x in functions.items()]
        return None
    else:
        return 'plot({})'.format(input_repr)


class GraphType(enum.Enum):
    xy = 0
    parametric = 1
    polar = 2


graph_handler: dict[GraphType, tuple[Callable[[float, float], float], Callable[[float, float], float]]] = {
    GraphType.xy: (lambda x, y: x, lambda x, y: y),
    GraphType.parametric: (lambda x, y: x, lambda x, y: y),
    GraphType.polar: (lambda theta, r: float(r * sympy.cos(theta)), lambda theta, r: float(r * sympy.sin(theta)))
}


def determine_graph_type(key: str) -> GraphType:
    if key.startswith('r'):
        return GraphType.polar
    elif key.startswith('p'):
        return GraphType.parametric
    return GraphType.xy


def eval_plot(components, parameters=None):
    def get_variable(variables):
        if len(variables) > 1:
            raise ValueError("Cannot plot multivariate function")
        if len(variables) == 0:
            return sympy.Symbol('x')
        return list(variables)[0]

    if parameters is None:
        parameters = {}
    from sympy.plotting.plot import LineOver1DRangeSeries, Parametric2DLineSeries
    functions = components["input_evaluated"]
    if isinstance(functions, list):
        func_type_list: list[tuple[Any, GraphType]] = [(f, GraphType.xy) for f in functions]
    elif isinstance(functions, dict):
        func_type_list = [(f, determine_graph_type(key)) for key, f in functions.items()]
    else:
        func_type_list = [(functions, GraphType.xy)]

    variable = 'x'
    graphs = []
    for func, graph_type in func_type_list:
        if graph_type == GraphType.parametric:
            x_func, y_func = func
            x_vars, y_vars = x_func.free_symbols, y_func.free_symbols
            if x_vars != y_vars:
                raise ValueError("Both functions in a parametric plot must have the same variable")
            variable = get_variable(x_vars.union(y_vars))
            graph_range = (variable, parameters.get('tmin', 0), parameters.get('tmax', 10))
            series = Parametric2DLineSeries(x_func, y_func, graph_range, nb_of_points=150)
        else:
            variable = get_variable(func.free_symbols)
            if graph_type == GraphType.xy:
                graph_range = (variable, parameters.get('xmin', -10), parameters.get('xmax', 10))
            else:
                graph_range = (variable, parameters.get('tmin', 0), parameters.get('tmax', 2 * sympy.pi))
            series = LineOver1DRangeSeries(func, graph_range, nb_of_points=150)
        series = list(series.get_segments())  # returns a list of [[x,y], [next_x, next_y]] pairs

        xvalues = []
        yvalues = []

        def limit_y(y):
            CEILING = 1e8
            if y > CEILING:
                y = CEILING
            if y < -CEILING:
                y = -CEILING
            return y

        x_transform, y_transform = graph_handler[graph_type]
        series.append([series[-1][1], None])
        for point in series:
            if point[0][1] is None:
                continue
            x = point[0][0]
            y = limit_y(point[0][1])
            xvalues.append(x_transform(x, y))
            yvalues.append(y_transform(x, y))

        graphs.append({
            'function': sympy.jscode(sympy.sympify(func)),
            'points': {
                'x': xvalues,
                'y': yvalues
            }
        })
    return repr(variable), graphs


def eval_factorization(components, parameters=None):
    number = components["input_evaluated"]
    return sympy.ntheory.factorint(number)


def eval_integral(components, parameters=None):
    return sympy.integrate(components['integrand'], *components['limits'])


def eval_integral_manual(components, parameters=None):
    return sympy.integrals.manualintegrate.manualintegrate(components['integrand'], components['variable'])


def eval_diffsteps(components, parameters=None):
    function = components.get('function', components['input_evaluated'])
    return gamma.diffsteps.print_json_steps(function, components['variable'])


def eval_intsteps(components, parameters=None):
    integrand = components.get('integrand', components['input_evaluated'])
    return gamma.intsteps.print_json_steps(integrand, components['variable'])


# https://www.python.org/dev/peps/pep-0257/
def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def eval_function_docs(components, parameters=None):
    docstring = trim(components["input_evaluated"].__doc__)
    return docutils.core.publish_parts(docstring, writer_name='html4css1',
                                       settings_overrides={'_disable_config': True})['html_body']


def eval_truth_table(components, parameters=None):
    expr = components["input_evaluated"]
    variables = sorted(expr.atoms(sympy.Symbol), key=str)

    result = []
    for combination in itertools.product([True, False], repeat=len(variables)):
        result.append(combination + (expr.subs(list(zip(variables, combination))),))
    return variables, result


def eval_approximator(components, parameters=None):
    if parameters is None:
        raise ValueError
    digits = parameters.get('digits', 10)
    return components['input_evaluated'], digits


# Result cards

all_cards: dict[str, ResultCard] = {
    'result': ResultCard('Result', None, None, format_input=lambda line, result, components: components['expression']),
    'roots': ResultCard(
        "Roots",
        "solve(%s, {_var})",
        lambda statement, var, *args: var,
        format_output=format_list),

    'integral': ResultCard(
        "Integral",
        "integrate(%s, {_var})",
        sympy.Integral),

    'integral_fake': ResultCard(
        "Integral",
        "integrate(%s, {_var})",
        lambda i, var: sympy.Integral(i, *var),
        eval_method=eval_integral,
        format_input=format_integral
    ),

    'integral_manual': ResultCard(
        "Integral",
        "manualintegrate(%s, {_var})",
        sympy.Integral),

    'integral_manual_fake': ResultCard(
        "Integral",
        "manualintegrate(%s, {_var})",
        lambda i, var: sympy.Integral(i, *var),
        eval_method=eval_integral_manual,
        format_input=format_integral
    ),

    'diff': ResultCard("Derivative",
                       "diff(%s, {_var})",
                       sympy.Derivative),

    'diffsteps': ResultCard(
        "Derivative Steps",
        "diff(%s, {_var})",
        format_output=format_steps,
        eval_method=eval_diffsteps),

    'intsteps': ResultCard(
        "Integral Steps",
        "integrate(%s, {_var})",
        format_output=format_steps,
        eval_method=eval_intsteps,
        format_input=format_integral),

    'series': ResultCard(
        "Series expansion around 0",
        "series(%s, {_var}, 0, 10)"),

    'digits': ResultCard(
        "Digits in base-10 expansion of number",
        "len(str(%s))",
        format_input=format_long_integer),

    'factorization': ResultCard(
        "Factors",
        "factorint(%s)",
        applicable=lambda components: components['input_evaluated'] > 0,
        format_input=format_long_integer,
        format_output=format_dict_title("Factor", "Times"),
        eval_method=eval_factorization),

    'factorizationDiagram': ResultCard(
        "Factorization Diagram",
        "factorint(%s)",
        applicable=lambda components: 0 < components['input_evaluated'] <= 256,
        format_output=format_factorization_diagram,
        eval_method=eval_factorization),

    'float_approximation': ResultCard(
        "Floating-point approximation",
        "(%s).evalf({digits})",
        parameters=['digits']),

    'fractional_approximation': ResultCard(
        "Fractional approximation",
        "nsimplify(%s)"),

    'absolute_value': ResultCard(
        "Absolute value",
        "Abs(%s)",
        lambda s, *args: sympy.Abs(s, evaluate=False)),

    'polar_angle': ResultCard(
        "Angle in the complex plane",
        "atan2(*(%s).as_real_imag()).evalf()",
        lambda s, *args: sympy.atan2(*s.as_real_imag())),

    'conjugate': ResultCard(
        "Complex conjugate",
        "conjugate(%s)",
        lambda s, *args: sympy.conjugate(s)),

    'trigexpand': ResultCard(
        "Alternate form",
        "(%s).expand(trig=True)",
        lambda statement, var, *args: statement),

    'trigsimp': ResultCard(
        "Alternate form",
        "trigsimp(%s)",
        lambda statement, var, *args: statement),

    'trigsincos': ResultCard(
        "Alternate form",
        "(%s).rewrite(csc, sin, sec, cos, cot, tan)",
        lambda statement, var, *args: statement
    ),

    'trigexp': ResultCard(
        "Alternate form",
        "(%s).rewrite(sin, exp, cos, exp, tan, exp)",
        lambda statement, var, *args: statement
    ),

    'plot': ResultCard(
        "Plot",
        "plot(%s)",
        format_input=format_plot_input,
        format_output=format_plot,
        eval_method=eval_plot,
        parameters=['xmin', 'xmax', 'tmin', 'tmax', 'pmin', 'pmax']),

    'function_docs': ResultCard(
        "Documentation",
        "help(%s)",
        eval_method=eval_function_docs,
        format_output=format_document
    ),

    'root_to_polynomial': ResultCard(
        "Polynomial with this root",
        "minpoly(%s)",
    ),

    'matrix_inverse': ResultCard(
        "Inverse of matrix",
        "(%s).inv()",
        lambda statement, var, *args: sympy.Pow(statement, -1, evaluate=False),
    ),

    'matrix_eigenvals': ResultCard(
        "Eigenvalues",
        "(%s).eigenvals()",
        format_output=format_dict_title("Eigenvalue", "Multiplicity")
    ),

    'matrix_eigenvectors': ResultCard(
        "Eigenvectors",
        "(%s).eigenvects()",
        format_output=format_list
    ),

    'satisfiable': ResultCard(
        "Satisfiability",
        "satisfiable(%s)",
        format_output=format_dict_title('Variable', 'Possible Value')
    ),

    'truth_table': ResultCard(
        "Truth table",
        "%s",
        eval_method=eval_truth_table,
        format_output=format_truth_table
    ),

    'doit': ResultCard("Result", "(%s).doit()"),

    'approximator': ResultCard(
        "Approximator_NOT_USER_VISIBLE",
        "%s",
        eval_method=eval_approximator,
        format_output=format_approximator
    ),
    'is_prime': is_prime_card,
    'totient': totient_card,
    'roman_numeral': roman_numeral_card,
    'binary_form': binary_form_card,
    'chinese_numeral': chinese_numeral_card,
    'modulo': modulo_card,
}


def get_card(name: str) -> ResultCard:
    return all_cards[name]


all_cards['trig_alternate'] = MultiResultCard(
    "Alternate forms",
    get_card('trigexpand'),
    get_card('trigsimp'),
    get_card('trigsincos'),
    get_card('trigexp')
)

all_cards['integral_alternate'] = MultiResultCard(
    "Antiderivative forms",
    get_card('integral'),
    get_card('integral_manual')
)

all_cards['integral_alternate_fake'] = MultiResultCard(
    "Antiderivative forms",
    get_card('integral_fake'),
    get_card('integral_manual_fake')
)

learn_more_sets: dict[str, list[str]] = {
    'rsolve': [
        'https://en.wikipedia.org/wiki/Recurrence_relation',
        'https://mathworld.wolfram.com/RecurrenceEquation.html',
        'https://docs.sympy.org/latest/modules/solvers/solvers.html#module-sympy.solvers.recurr'
    ]
}


def find_learn_more_set(function_name: str):
    urls = learn_more_sets.get(function_name)
    if urls is None:
        return None
    return Reference(links=urls)
