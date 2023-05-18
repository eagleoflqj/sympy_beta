from abc import ABC
from dataclasses import dataclass
from functools import reduce
from typing import NamedTuple

from sympy import (
    Add,
    Derivative,
    Dummy,
    E,
    Eq,
    Expr,
    Function,
    Mul,
    Pow,
    Symbol,
    exp,
    log,
    ratsimp,
    simplify,
)
from sympy.core.function import AppliedUndef
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.strategies.core import switch

from .stepprinter import JSONPrinter, functionnames, replace_u_var


@dataclass
class Rule(ABC):
    function: Expr
    variable: Symbol


@dataclass
class ConstantRule(Rule):
    pass


@dataclass
class ConstantTimesRule(Rule):
    constant: Expr
    other: Expr
    substep: Rule


@dataclass
class PowerRule(Rule):
    exp: Expr


@dataclass
class AddRule(Rule):
    substeps: list[Rule]


@dataclass
class MulRule(Rule):
    terms: tuple[Expr]
    substeps: list[Rule]


@dataclass
class DivRule(Rule):
    numerator: Expr
    denominator: Expr
    numerstep: Rule
    denomstep: Rule


@dataclass
class ChainRule(Rule):
    substep: Rule
    inner: Expr
    u_var: Symbol
    innerstep: Rule


@dataclass
class TrigRule(Rule):
    pass


@dataclass
class ExpRule(Rule):
    base: Expr


@dataclass
class LogRule(Rule):
    pass


@dataclass
class FunctionRule(Rule):
    pass


@dataclass
class RewriteRule(Rule):
    rewritten: Expr
    substep: Rule


class DerivativeInfo(NamedTuple):
    expr: Expr
    symbol: Symbol


def power_rule(derivative: DerivativeInfo):
    expr, symbol = derivative.expr, derivative.symbol
    base, _exp = expr.as_base_exp()

    if not base.has(symbol):
        if isinstance(_exp, Symbol):
            return ExpRule(expr, symbol, base)
        u = Dummy()
        f = base ** u
        return ChainRule(
            expr, symbol,
            ExpRule(f, u, base),
            _exp, u,
            diff_steps(_exp, symbol)
        )
    if not _exp.has(symbol):
        if isinstance(base, Symbol):
            return PowerRule(expr, symbol, _exp)
        u = Dummy()
        f = u ** _exp
        return ChainRule(
            expr, symbol,
            PowerRule(f, u, _exp),
            base, u,
            diff_steps(base, symbol)
        )
    rewritten = exp(_exp*log(base))
    return RewriteRule(
        expr, symbol,
        rewritten,
        diff_steps(rewritten, symbol)
    )


def add_rule(derivative: DerivativeInfo):
    expr, symbol = derivative.expr, derivative.symbol
    return AddRule(
        expr, symbol,
        [diff_steps(arg, symbol) for arg in expr.args]
    )


def constant_rule(derivative: DerivativeInfo):
    expr, symbol = derivative.expr, derivative.symbol
    return ConstantRule(expr, symbol)


def mul_rule(derivative: DerivativeInfo):
    expr, symbol = derivative
    terms = expr.args

    coeff, f = expr.as_independent(symbol)

    if coeff != 1:
        return ConstantTimesRule(expr, symbol, coeff, f, diff_steps(f, symbol))

    numerator, denominator = expr.as_numer_denom()
    if denominator != 1:
        return DivRule(
            expr, symbol,
            numerator, denominator,
            diff_steps(numerator, symbol),
            diff_steps(denominator, symbol)
        )

    return MulRule(expr, symbol, terms, [diff_steps(g, symbol) for g in terms])


def trig_rule(derivative: DerivativeInfo):
    expr, symbol = derivative
    arg = expr.args[0]
    if isinstance(arg, Symbol):
        return TrigRule(expr, symbol)
    u = Dummy()
    return ChainRule(
        expr, symbol,
        TrigRule(expr.func(u), u),
        arg, u, diff_steps(arg, symbol)
    )

def exp_rule(derivative: DerivativeInfo):
    expr, symbol = derivative
    _exp = expr.args[0]
    if isinstance(_exp, Symbol):
        return ExpRule(expr, symbol, E)
    u = Dummy()
    f = exp(u)
    return ChainRule(
        expr, symbol,
        ExpRule(f, u, E),
        _exp, u, diff_steps(_exp, symbol)
    )


def log_rule(derivative: DerivativeInfo):
    expr, symbol = derivative
    arg = expr.args[0]
    if isinstance(arg, Symbol):
        return LogRule(expr, symbol)
    u = Dummy()
    return ChainRule(
        expr, symbol,
        LogRule(log(u), u), arg, u, diff_steps(arg, symbol)
    )


def function_rule(derivative: DerivativeInfo):
    expr, symbol = derivative
    arg = expr.args[0]   # XXX: only works for unary function
    if isinstance(arg, Symbol):
        return FunctionRule(expr, symbol)
    u = Dummy()
    return ChainRule(
        expr, symbol,
        FunctionRule(expr.func(u), u), arg, u, diff_steps(arg, symbol)
    )


def diff_steps(expr: Expr, symbol: Symbol):
    deriv = DerivativeInfo(expr, symbol)

    def key(deriv):
        expr = deriv.expr
        if isinstance(expr, TrigonometricFunction):
            return TrigonometricFunction
        elif isinstance(expr, AppliedUndef):
            return AppliedUndef
        elif not expr.has(symbol):
            return 'constant'
        else:
            return expr.func

    return switch(key, {
        Pow: power_rule,
        Symbol: power_rule,
        Dummy: power_rule,
        Add: add_rule,
        Mul: mul_rule,
        TrigonometricFunction: trig_rule,
        exp: exp_rule,
        log: log_rule,
        AppliedUndef: function_rule,
        'constant': constant_rule
    })(deriv)


def diff(rule):
    return rule.function.diff(rule.variable)


class DiffPrinter(JSONPrinter):
    def print_rule(self, rule: Rule):
        handlers = {
            ConstantRule: self.print_Constant,
            ConstantTimesRule: self.print_ConstantTimes,
            PowerRule: self.print_Power,
            AddRule: self.print_Add,
            MulRule: self.print_Mul,
            DivRule: self.print_Div,
            ChainRule: self.print_Chain,
            TrigRule: self.print_Trig,
            ExpRule: self.print_Exp,
            LogRule: self.print_Log,
            FunctionRule: self.print_Function,
            RewriteRule: self.print_Rewrite,
        }
        handler = handlers[type(rule)]  # type: ignore
        handler(rule)

    def print_Power(self, rule: PowerRule):
        with self.new_step():
            self.append(self.format_text("Apply the power rule: "),
                        self.format_math(rule.function),
                        self.format_text(" goes to "),
                        self.format_math(diff(rule)))

    def print_Constant(self, rule: ConstantRule):
        with self.new_step():
            self.append(self.format_text("The derivative of the constant "),
                        self.format_math(rule.function),
                        self.format_text(" is zero."))

    def print_ConstantTimes(self, rule: ConstantTimesRule):
        with self.new_step():
            self.append(self.format_text("The derivative of a constant times a function "
                                         "is the constant times the derivative of the function."))
            with self.new_level():
                self.print_rule(rule.substep)
            self.append(self.format_text("So, the result is: "),
                        self.format_math(diff(rule)))

    def print_Add(self, rule: AddRule):
        with self.new_step():
            self.append(self.format_text("Differentiate "),
                        self.format_math(rule.function),
                        self.format_text(" term by term:"))
            with self.new_level():
                for substep in rule.substeps:
                    self.print_rule(substep)
            self.append(self.format_text("The result is: "),
                        self.format_math(diff(rule)))

    def print_Mul(self, rule: MulRule):
        with self.new_step():
            self.append(self.format_text("Apply the product rule: "),
                        self.format_math(rule.function))

            fnames = [Function(n)(rule.variable) for n in functionnames(len(rule.terms))]
            derivatives = [Derivative(f, rule.variable) for f in fnames]
            ruleform = []
            for index in range(len(rule.terms)):
                buf = []
                for i in range(len(rule.terms)):
                    if i == index:
                        buf.append(derivatives[i])
                    else:
                        buf.append(fnames[i])
                ruleform.append(reduce(lambda a, b: a * b, buf))
            self.append(self.format_math_display(
                Eq(Derivative(reduce(lambda a, b: a * b, fnames), rule.variable), sum(ruleform),
                         evaluate=False)))

            for fname, deriv, term, substep in zip(fnames, derivatives, rule.terms, rule.substeps):
                self.append(self.format_math(Eq(fname, term, evaluate=False)),
                            self.format_text("; to find "),
                            self.format_math(deriv),
                            self.format_text(":"))
                with self.new_level():
                    self.print_rule(substep)
            self.append(self.format_text("The result is: "),
                        self.format_math(diff(rule)))

    def print_Div(self, rule: DivRule):
        with self.new_step():
            f, g = rule.numerator, rule.denominator
            x = rule.variable
            ff = Function("f")(x)
            gg = Function("g")(x)
            qrule_left = Derivative(ff / gg, rule.variable)
            qrule_right = ratsimp((Function("f")(x) / Function("g")(x)).diff())
            qrule = Eq(qrule_left, qrule_right, evaluate=False)
            self.append(self.format_text("Apply the quotient rule, which is:"))
            self.append(self.format_math_display(qrule))
            self.append(self.format_math(Eq(ff, f, evaluate=False)),
                        self.format_text(" and "),
                        self.format_math(Eq(gg, g, evaluate=False)))
            self.append(self.format_text("To find "),
                        self.format_math(ff.diff(rule.variable)),
                        self.format_text(":"))
            with self.new_level():
                self.print_rule(rule.numerstep)
            self.append(self.format_text("To find "),
                        self.format_math(gg.diff(rule.variable)),
                        self.format_text(":"))
            with self.new_level():
                self.print_rule(rule.denomstep)
            self.append(self.format_text("Now plug in to the quotient rule:"))
            self.append(self.format_math(diff(rule)))

    def print_Chain(self, rule: ChainRule):
        with self.new_step(), self.new_u_vars() as (u, du):
            self.append(self.format_text("Let "),
                        self.format_math(Eq(u, rule.inner, evaluate=False)))
            self.print_rule(replace_u_var(rule.substep, rule.u_var, u))
        with self.new_step():
            self.append(self.format_text("Then, apply the chain rule. Multiply by "),
                        self.format_math(Derivative(rule.inner, rule.variable)),
                        self.format_text(":"))
            if isinstance(rule.innerstep, FunctionRule):
                self.append(self.format_math_display(diff(rule)))
            else:
                with self.new_level():
                    self.print_rule(rule.innerstep)
                self.append(self.format_text("The result of the chain rule is:"))
                self.append(self.format_math_display(diff(rule)))

    def print_Trig(self, rule: TrigRule):
        with self.new_step():
            self.append(self.format_math_display(Eq(
                Derivative(rule.function, rule.variable),
                diff(rule),
                evaluate=False
            )))

    def print_Exp(self, rule: ExpRule):
        with self.new_step():
            if rule.base == E:
                self.append(self.format_text("The derivative of "),
                            self.format_math(exp(rule.variable)),
                            self.format_text(" is itself."))
            else:
                self.append(self.format_math(Eq(Derivative(rule.function, rule.variable), diff(rule),
                                                      evaluate=False)))

    def print_Log(self, rule: LogRule):
        with self.new_step():
            self.append(self.format_text("The derivative of "),
                        self.format_math(rule.function),
                        self.format_text(" is "),
                        self.format_math(diff(rule)))

    def print_Rewrite(self, rule: RewriteRule):
        with self.new_step():
            self.append(self.format_text("Rewrite the function to be differentiated:"))
            self.append(self.format_math_display(Eq(rule.function, rule.rewritten, evaluate=False)))
            self.print_rule(rule.substep)

    def print_Function(self, rule: FunctionRule):
        with self.new_step():
            self.append(self.format_text("Trivial:"))
            self.append(self.format_math_display(Eq(Derivative(rule.function, rule.variable), diff(rule),
                                                          evaluate=False)))

    def finalize(self):
        answer = diff(self.rule)
        if answer:
            simp = simplify(answer)
            if simp != answer:
                answer = simp
                with self.new_step():
                    self.append(self.format_text("Now simplify:"))
                    self.append(self.format_math_display(simp))
        return {
            'content': {'level': self.stack},
            'answer': self.format_math_display(answer)
        }


def print_json_steps(function, symbol):
    a = DiffPrinter(diff_steps(function, symbol))
    return a.finalize()
