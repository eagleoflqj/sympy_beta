import ast
from typing import Any, cast

import sympy
from sympy.core.function import FunctionClass
from sympy.parsing.sympy_parser import eval_expr, stringify_expr

from data_type import Tex
from extension.util import DICT
from gamma.dispatch import find_result_set
from gamma.evaluator import namespace, transformations
from gamma.resultsets import find_learn_more_set, format_by_type, get_card
from gamma.utils import OTHER_SYMPY_FUNCTIONS, is_approximatable_constant, latexify, mathjax_latex, removeSymPy


class SymPyGamma:
    def __init__(self, expression: str, variable: str | None = None):
        self.expression = expression
        self.variable = variable
        self.parsed = stringify_expr(expression, {}, namespace, transformations)
        self.evaluated = eval_expr(self.parsed, {}, namespace)
        self.top_node = cast(ast.Expr, ast.parse(self.parsed).body[0]).value

    def disambiguate(self) -> DICT | None:
        if isinstance(self.top_node, ast.Call) and isinstance(self.top_node.func, ast.Name) \
                and self.top_node.func.id == 'factor' and self.top_node.args:
            arg = self.top_node.args[0]
            if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == 'Integer':
                return {
                    'ambiguity': 'factorint({})'.format(cast(ast.Constant, arg.args[0]).value),
                    'description': [{'type': 'Expression', 'value': 'factor'},
                                    {'type': 'Text', 'value': ' factors polynomials, while '},
                                    {'type': 'Expression', 'value': 'factorint'},
                                    {'type': 'Text', 'value': ' factors integers.'}]
                }
        return None

    def get_cards(self):
        top_func_name = self.top_node.func.id if isinstance(self.top_node, ast.Call)\
                                                 and isinstance(self.top_node.func, ast.Name) else ''

        first_func = namespace.get(top_func_name)
        is_imperative = first_func is not None and not isinstance(first_func, FunctionClass) \
            and not isinstance(first_func, sympy.Atom) and top_func_name[0].islower() \
            and top_func_name not in OTHER_SYMPY_FUNCTIONS

        convert_input, cards = find_result_set(top_func_name, self.evaluated, is_imperative)
        components = convert_input(self.top_node, self.evaluated)
        components['expression'] = self.expression

        return components, cards, top_func_name if is_imperative else ''

    def eval(self) -> DICT:
        components, cards, top_func_name = self.get_cards()
        if self.variable is not None:
            components['variable'] = sympy.Symbol(self.variable)

        sympy_input = removeSymPy(self.parsed)
        if top_func_name:
            latex_input = Tex(tex=latexify(self.top_node))
        else:
            latex_input = mathjax_latex(self.evaluated, digits=None)

        result: list[dict[str, Any]] = []

        ambiguity = self.disambiguate()
        if ambiguity is not None:
            result.append(ambiguity)

        result.append({
            "title": "SymPy",
            "input": sympy_input,
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
        if not cards and top_func_name:
            result.append({
                'title': 'Result',
                'input': sympy_input if top_func_name else str(self.evaluated),
                'output': format_by_type(self.evaluated, top_func_name, self.top_node, mathjax_latex)
            })
        elif is_approximatable_constant(self.evaluated):
            cards = ['float_approximation'] + cards

        if top_func_name not in ('factor', 'simplify'):
            simplified = sympy.simplify(self.evaluated) if isinstance(self.evaluated, sympy.Basic) else None
            if simplified is not None and simplified != self.evaluated:
                result.append({"title": "Simplification", "input": repr(simplified),
                               "output": mathjax_latex(simplified, digits=None)})

        for card_name in cards:
            card = get_card(card_name)
            card_data = card.get_data(card_name, components)
            if card_data:
                result.append(card_data)

        learn_more = find_learn_more_set(top_func_name)
        if learn_more:
            result.append({
                "title": "Learn More",
                "input": '',
                "output": learn_more
            })
        return {'result': result}

    def eval_card(self, card_name: str, parameters=None):
        card = get_card(card_name)
        components, _, _ = self.get_cards()
        result = card.eval(components, parameters)
        return card.format_output(result)
