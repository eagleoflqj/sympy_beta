from __future__ import annotations
import ast
import traceback

import sympy
from sympy.core.function import FunctionClass

from gamma.utils import latexify, removeSymPy, OTHER_SYMPY_FUNCTIONS
from gamma.evaluator import eval_input, namespace
from gamma.dispatch import find_result_set, is_function_handled
from gamma.resultsets import get_card, format_by_type, find_learn_more_set


def latex(expr: sympy.Basic | str | int) -> str:
    # sympy.latex('') == '\\mathtt{\\text{}}'
    if expr == '':
        return ''
    if isinstance(expr, sympy.Basic):
        # solveset(sin(x)) click More Digits
        expr = expr.replace(sympy.Symbol('_n'), sympy.Dummy('n'))
    return sympy.latex(expr)


def mathjax_latex(*args, digits=15):
    tex_code = []
    for obj in args:
        if hasattr(obj, 'as_latex'):
            tex_code.append(obj.as_latex())
        else:
            tex_code.append(latex(obj))

    result = {
        'type': 'Tex',
        'tex': ''.join(tex_code)
    }
    if len(args) == 1:
        obj = args[0]
        if isinstance(obj, sympy.Basic) and not obj.free_symbols \
                and not obj.is_Integer and not obj.is_Float \
                and obj.is_finite is not False and hasattr(obj, 'evalf'):
            result.update({
                'numeric': True,
                'expression': repr(obj),
                'approximation': latex(obj.evalf(digits))
            })
    return result


class SymPyGamma:

    def eval(self, s: str, variable: str | None = None):
        try:
            parsed, top_node, evaluated = eval_input(s)
            cards = self.prepare_cards(parsed, top_node, evaluated, variable)
            return cards
        except Exception:
            return self.handle_error(s)

    @staticmethod
    def handle_error(s: str):
        trace = traceback.format_exc()
        return [
            {"title": "Error", "input": s, "error": trace}
        ]

    @staticmethod
    def disambiguate(top_node):
        if isinstance(top_node, ast.Call) and isinstance(top_node.func, ast.Name) \
                and top_node.func.id == 'factor' and top_node.args:
            arg = top_node.args[0]
            if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == 'Integer':
                return {
                    'ambiguity': 'factorint({})'.format(arg.args[0].value),
                    'description': [{'type': 'Expression', 'value': 'factor'},
                                    {'type': 'Text', 'value': ' factors polynomials, while '},
                                    {'type': 'Expression', 'value': 'factorint'},
                                    {'type': 'Text', 'value': ' factors integers.'}]
                }
        return None

    def get_cards(self, top_node, evaluated):
        is_applied = isinstance(top_node, ast.Call)
        top_func_name = top_node.func.id if is_applied and isinstance(top_node.func, ast.Name) else ''

        first_func = namespace.get(top_func_name)
        is_function = first_func and not isinstance(first_func, FunctionClass) \
            and not isinstance(first_func, sympy.Atom) and top_func_name and top_func_name[0].islower() \
            and top_func_name not in OTHER_SYMPY_FUNCTIONS

        convert_input, cards = find_result_set(top_func_name, evaluated)

        components = convert_input(top_node, evaluated)
        if 'input_evaluated' in components:
            evaluated = components['input_evaluated']

        return components, cards, evaluated, top_func_name if (is_function and is_applied) else ''

    def prepare_cards(self, parsed, top_node, evaluated, variable: str | None = None):
        components, cards, evaluated, top_func_name = self.get_cards(top_node, evaluated)
        if variable is not None:
            components['variable'] = sympy.Symbol(variable)

        if top_func_name:
            latex_input = {
                'type': 'Tex',
                'tex': latexify(parsed)
            }
        else:
            latex_input = mathjax_latex(evaluated)

        result = []

        ambiguity = self.disambiguate(top_node)
        if ambiguity is not None:
            result.append(ambiguity)

        result.append({
            "title": "SymPy",
            "input": removeSymPy(parsed),
            "output": latex_input
        })

        if any(get_card(c).is_multivariate() for c in cards):
            result[-1].update({
                "num_variables": len(components['variables']),
                "variables": list(map(repr, components['variables'])),
                "variable": repr(components['variable'])
            })

        # If no result cards were found, but the top-level call is to a
        # function, then add a special result card to show the result
        if not cards and not components['variable'] and top_func_name:
            result.append({
                'title': 'Result',
                'input': removeSymPy(parsed),
                'output': format_by_type(evaluated, top_func_name, top_node, mathjax_latex)
            })
        else:
            var = components['variable']

            # If the expression is something like 'lcm(2x, 3x)', display the
            # result of the function before the rest of the cards
            if top_func_name and not is_function_handled(top_func_name):
                result.append(
                    {"title": "Result", "input": "",
                     "output": format_by_type(evaluated, top_func_name, top_node, mathjax_latex)})

            simplified = sympy.simplify(evaluated) if isinstance(evaluated, sympy.Basic) else None
            if simplified is not None and simplified != evaluated:
                result.append(
                    {"title": "Simplification", "input": repr(simplified),
                     "output": mathjax_latex(simplified)})
            elif top_func_name == 'simplify':
                result.append(
                    {"title": "Simplification", "input": "",
                     "output": mathjax_latex(evaluated)})

            for card_name in cards:
                card = get_card(card_name)

                if not card:
                    continue

                result.append({
                    'card': card_name,
                    'variable': repr(var),
                    'title': card.format_title(evaluated),
                    'input': card.format_input(repr(evaluated), components),
                    'pre_output': latex(
                        card.pre_output_function(evaluated, var)),
                    'parameters': card.card_info.get('parameters', [])
                })

            if top_func_name:
                learn_more = find_learn_more_set(top_func_name)
                if learn_more:
                    result.append({
                        "title": "Learn More",
                        "input": '',
                        "output": learn_more
                    })
        return result

    def eval_card(self, card_name: str, expression: str, variable="None", parameters=None):
        card = get_card(card_name)
        _, top_node, evaluated = eval_input(expression)
        variable = sympy.Symbol(variable)
        components, _, evaluated, _ = self.get_cards(top_node, evaluated)
        components['variable'] = variable
        result = card.eval(components, parameters)
        return card.format_output(result, mathjax_latex)
