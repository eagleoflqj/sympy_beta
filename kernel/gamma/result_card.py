import sympy

from gamma.dispatch import DICT
from gamma.evaluator import namespace


class ResultCard:
    """
    Operations to generate a result card.

    title -- Title of the card

    result_statement -- Statement evaluated to get result

    pre_output_function -- Takes input expression and a symbol, returns a
    SymPy object
    """
    def __init__(self, title, result_statement, pre_output, **kwargs):
        self.card_info = kwargs
        self.title = title
        self.result_statement = result_statement
        self.pre_output = pre_output or no_pre_output

    def eval(self, components: DICT, parameters):
        if parameters is None:
            parameters = {}
        else:
            parameters = parameters.copy()

        parameters = self.default_parameters(parameters)

        for component, val in components.items():
            parameters[component] = val

        variable = components['variable']

        line = self.result_statement.format(_var=variable, **parameters)
        line = line % components['input_evaluated']
        return sympy.parse_expr(line, global_dict=namespace)

    def format_input(self, components: DICT, **parameters):
        if parameters is None:
            parameters = {}
        parameters = self.default_parameters(parameters)
        input_repr = repr(components['input_evaluated'])
        variable = components['variable']
        if 'format_input' in self.card_info:
            return self.card_info['format_input'](
                self.result_statement, input_repr, components)
        return self.result_statement.format(_var=variable, **parameters) % input_repr

    def format_output(self, output, formatter):
        if 'format_output' in self.card_info:
            return self.card_info['format_output'](output, formatter)
        return formatter(output)

    def format_title(self, input_evaluated):
        if self.card_info.get('format_title'):
            return self.card_info['format_title'](self.title, input_evaluated)
        return self.title

    def is_multivariate(self):
        return self.card_info.get('multivariate', True)

    def default_parameters(self, kwargs):
        if 'parameters' in self.card_info:
            for arg in self.card_info['parameters']:
                kwargs.setdefault(arg, '')
        return kwargs

    def __repr__(self):
        return "<ResultCard '{}'>".format(self.title)


class FakeResultCard(ResultCard):
    """ResultCard whose displayed expression != actual code.

    Used when creating the result to be displayed involves code that a user
    would not normally need to do, e.g. calculating plot points (where a
    user would simply use ``plot``)."""

    def eval(self, components: DICT, parameters=None):
        if parameters is None:
            parameters = {}
        return self.card_info['eval_method'](components, parameters)


class MultiResultCard(ResultCard):
    """Tries multiple statements and displays the first that works."""

    def __init__(self, title, *cards):
        super().__init__(title, '', lambda *args: '')
        self.cards = cards
        self.cards_used = []

    def eval(self, components, parameters):
        self.cards_used = []
        results = []

        # TODO Implicit state is bad, come up with better API
        # in particular a way to store variable, cards used
        for card in self.cards:
            try:
                result = card.eval(components, parameters)
            except ValueError:
                continue
            if result is not None:
                if not any(result == r[1] for r in results):
                    self.cards_used.append(card)
                    results.append((card, result))
        if results:
            self.components = components
            return results
        return "None"

    def format_input(self, components):
        return None

    def format_output(self, output, formatter):
        if not isinstance(output, list):
            return output
        return {
            'type': 'MultiResult',
            'results': [{
                'input': card.format_input(self.components),
                'output': card.format_output(result, formatter)
            } for card, result in output]
        }


def no_pre_output(*args):
    return ""
