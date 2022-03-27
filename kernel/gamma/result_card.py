from __future__ import annotations

from typing import Any, Callable

import sympy

from api.data_type import Dict
from gamma.dispatch import DICT
from gamma.evaluator import namespace
from gamma.utils import latex


class ResultCard:
    """
    Operations to generate a result card.

    title -- Title of the card

    result_statement -- Statement evaluated to get result

    pre_output_function -- Takes input expression and a symbol, returns a
    SymPy object
    """
    def __init__(self, title: str, result_statement: str | None, pre_output: Callable[[Any, Any], Any] | None = None,
                 applicable: Callable[[DICT], bool] | None = None,
                 format_input: Callable[[Any, Any, Any], str | list[str] | None] | None = None,
                 eval_method: Callable[[DICT, DICT | None], Any] | None = None,
                 format_output: Callable[..., Dict] | None = None, parameters: list[str] | None = None,
                 wiki: str | None = None):
        self.title = title
        self.result_statement = result_statement
        self.pre_output = pre_output
        self.applicable = applicable
        self._format_input = format_input
        self.eval_method = eval_method
        self._format_output = format_output
        self.parameters = parameters
        self.source: str | None = None
        self.wiki = wiki

    def eval(self, components: DICT, parameters):
        if self.eval_method:
            return self.eval_method(components, parameters)

        if parameters is None:
            parameters = {}
        else:
            parameters = parameters.copy()

        parameters = self.default_parameters(parameters)

        for component, val in components.items():
            parameters[component] = val

        variable = components['variable']

        line = self.result_statement.format(_var=variable, **parameters) % components['input_evaluated']\
            if self.result_statement is not None else components['expression']
        return sympy.parse_expr(line, global_dict=namespace)

    def format_input(self, components: DICT):
        parameters = self.default_parameters({})
        input_repr = repr(components['input_evaluated'])
        variable = components['variable']
        if self._format_input:
            return self._format_input(self.result_statement, input_repr, components)
        return None if self.result_statement is None \
            else self.result_statement.format(_var=variable, **parameters) % input_repr

    def format_output(self, output, formatter):
        if self._format_output:
            return self._format_output(output, formatter)
        return formatter(output)

    def is_multivariate(self):
        return False  # todo: whether multivariate depends on input: diff(x+y) is but diff(x+y, x) isn't

    def default_parameters(self, kwargs):
        if self.parameters:
            for arg in self.parameters:
                kwargs.setdefault(arg, '')
        return kwargs

    def get_data(self, card_name: str, components: DICT) -> DICT | None:
        if self.applicable and not self.applicable(components):
            return None
        data: DICT = {
            'name': card_name,
            'title': self.title
        }
        _input = self.format_input(components)
        if _input:
            data['input'] = _input
        var = components['variable']
        if var:
            data['variable'] = repr(var)
        if self.pre_output:
            data['pre_output'] = latex(self.pre_output(components['input_evaluated'], var))
        if self.parameters:
            data['parameters'] = self.parameters
        if self.source:
            data['source'] = self.source
        if self.wiki:
            data['wiki'] = self.wiki
        return data


class MultiResultCard(ResultCard):
    """Tries multiple statements and displays the first that works."""

    def __init__(self, title, *cards: ResultCard):
        super().__init__(title, None, lambda *args: '')
        self.cards = cards

    def eval(self, components: DICT, parameters):
        results = []
        for card in self.cards:
            result = card.eval(components, parameters)
            if result is not None:
                if not any(result == r[1] for r in results):
                    results.append((card, result))
        # TODO Implicit state is bad, come up with better API
        # in particular a way to store variable, cards used
        self.components = components
        return results

    def format_output(self, output, formatter):
        return {
            'type': 'MultiResult',
            'results': [{
                'input': card.format_input(self.components),
                'output': card.format_output(result, formatter)
            } for card, result in output]
        }
