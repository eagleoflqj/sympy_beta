import sympy
from sympy.integrals.manualintegrate import (AddRule, AlternativeRule, CompleteSquareRule, ConstantRule,
                                             ConstantTimesRule, CyclicPartsRule, DontKnowRule, ExpRule, PartsRule,
                                             PowerRule, RewriteRule, SqrtQuadraticDenomRule, SqrtQuadraticRule,
                                             TrigRule, TrigSubstitutionRule, URule, _manualintegrate, integral_steps)

from gamma.stepprinter import JSONPrinter, replace_u_var
from gamma.utils import DerivExpr, latex


def contains_dont_know(rule):
    if isinstance(rule, DontKnowRule):
        return True
    for val in rule._asdict().values():
        if isinstance(val, tuple):
            if contains_dont_know(val):
                return True
        elif isinstance(val, list):
            for item in val:
                if type(item) is tuple:  # PiecewiseRule
                    sub_rule = item[0]
                else:  # AlternativeRule
                    sub_rule = item
                if contains_dont_know(sub_rule):
                    return True
    return False


def filter_unknown_alternatives(rule):
    if isinstance(rule, AlternativeRule):
        alternatives = list([r for r in rule.alternatives if not contains_dont_know(r)])
        if not alternatives:
            alternatives = rule.alternatives
        return AlternativeRule(alternatives, rule.context, rule.symbol)
    return rule


class IntegralPrinter(JSONPrinter):
    def __init__(self, rule):
        super().__init__(rule)
        self.u_name = 'u'
        self.u = self.du = None

    def print_rule(self, rule):
        handlers = {
            ConstantRule: self.print_Constant,
            ConstantTimesRule: self.print_ConstantTimes,
            PowerRule: self.print_Power,
            AddRule: self.print_Add,
            URule: self.print_U,
            PartsRule: self.print_Parts,
            CyclicPartsRule: self.print_CyclicParts,
            TrigRule: self.print_Trig,
            ExpRule: self.print_Exp,
            AlternativeRule: self.print_Alternative,
            DontKnowRule: self.print_DontKnow,
            RewriteRule: self.print_Rewrite,
            TrigSubstitutionRule: self.print_TrigSubstitution,
            CompleteSquareRule: self.print_CompleteSquare,
            SqrtQuadraticRule: self.print_SqrtQuadratic,
            SqrtQuadraticDenomRule: self.print_SqrtQuadraticDenom,
        }
        handler = handlers.get(type(rule), self.print_simple)
        handler(rule)

    def print_Constant(self, rule):
        with self.new_step():
            self.append(self.format_text("The integral of a constant is the constant "
                                         "times the variable of integration:"))
            self.append(self.format_math_display(sympy.Eq(sympy.Integral(rule.constant, rule.symbol),
                                                          _manualintegrate(rule),
                                                          evaluate=False)))

    def print_ConstantTimes(self, rule):
        with self.new_step():
            self.append(self.format_text("The integral of a constant times a function "
                                         "is the constant times the integral of the function:"))
            self.append(self.format_math_display(sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                                                          rule.constant * sympy.Integral(rule.other, rule.symbol),
                                                          evaluate=False)))

            with self.new_level():
                self.print_rule(rule.substep)
            self.append(self.format_text("So, the result is: "),
                        self.format_math(_manualintegrate(rule)))

    def print_Power(self, rule):
        with self.new_step():
            self.append(self.format_text("The integral of "),
                        self.format_math(rule.symbol ** sympy.Symbol('n')),
                        self.format_text(" is "),
                        self.format_math((rule.symbol ** (1 + sympy.Symbol('n'))) / (1 + sympy.Symbol('n'))),
                        self.format_text(" when "),
                        self.format_math(sympy.Ne(sympy.Symbol('n'), -1)),
                        self.format_text(":"))
            self.append(self.format_math_display(sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                                                          _manualintegrate(rule),
                                                          evaluate=False)))

    def print_Add(self, rule):
        with self.new_step():
            self.append(self.format_text("Integrate term-by-term:"))
            for substep in rule.substeps:
                with self.new_level():
                    self.print_rule(substep)
            self.append(self.format_text("The result is: "),
                        self.format_math(_manualintegrate(rule)))

    def print_U(self, rule):
        with self.new_step(), self.new_u_vars() as (u, du):
            # commutative always puts the symbol at the end when printed
            dx = DerivExpr(rule.symbol.name)
            self.append(self.format_text("Let "),
                        self.format_math(sympy.Eq(u, rule.u_func, evaluate=False)),
                        self.format_text(', then '),
                        self.format_math(sympy.Eq(du, rule.u_func.diff(rule.symbol) * dx, evaluate=False)))
            self.append(self.format_text("Substitute:"))
            self.append(self.format_math_display(sympy.Integral(rule.substep.context, u)))

            with self.new_level():
                self.print_rule(replace_u_var(rule.substep, rule.symbol.name, u))

            self.append(self.format_text("Now substitute "),
                        self.format_math(u),
                        self.format_text(" back in:"))

            self.append(self.format_math_display(_manualintegrate(rule)))

    def print_Parts(self, rule):
        with self.new_step():
            self.append(self.format_text("Use integration by parts:"))
            u, v = sympy.Function('u')(rule.symbol), sympy.Function('v')(rule.symbol)
            du, dv, dx = DerivExpr('u'), DerivExpr('v'), DerivExpr('x')
            self.append(self.format_math_display(R"\int u \mathrm{d}v = uv - \int v \mathrm{d}u"))

            self.append(self.format_text("Let "),
                        self.format_math(sympy.Eq(u, rule.u, evaluate=False)),
                        self.format_text(" and "),
                        self.format_math(sympy.Eq(dv, rule.dv * dx, evaluate=False)))
            self.append(self.format_text("Then "),
                        self.format_math(sympy.Eq(du, rule.u.diff(rule.symbol) * dx, evaluate=False)))

            self.append(self.format_text("To find "),
                        self.format_math(v),
                        self.format_text(":"))

            with self.new_level():
                self.print_rule(rule.v_step)

            self.append(self.format_text("Now evaluate the sub-integral."))
            self.print_rule(rule.second_step)

    def print_CyclicParts(self, rule):
        with self.new_step():
            self.append(self.format_text("Use integration by parts, noting that the integrand"
                                         " eventually repeats itself."))
            u = sympy.Function('u')(rule.symbol)
            dv, dx = DerivExpr('v'), DerivExpr('x')
            current_integrand = rule.context
            total_result = sympy.S.Zero
            with self.new_level():
                sign = 1
                for rl in rule.parts_rules:
                    with self.new_step():
                        self.append(self.format_text("For the integrand "),
                                    self.format_math(current_integrand),
                                    self.format_text(":"))
                        self.append(self.format_text("Let "),
                                    self.format_math(sympy.Eq(u, rl.u, evaluate=False)),
                                    self.format_text(" and "),
                                    self.format_math(sympy.Eq(dv, rl.dv * dx, evaluate=False)))

                        v_f, du_f = _manualintegrate(rl.v_step), rl.u.diff(rule.symbol)

                        total_result += sign * rl.u * v_f
                        current_integrand = v_f * du_f

                        self.append(self.format_text("Then "),
                                    self.format_math(
                                        sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                                                 total_result - sign * sympy.Integral(current_integrand, rule.symbol),
                                                 evaluate=False)))
                        sign *= -1
                with self.new_step():
                    self.append(self.format_text("Notice that the integrand has repeated itself, so "
                                                 "move it to one side:"))
                    self.append(self.format_math_display(
                        sympy.Eq((1 - rule.coefficient) * sympy.Integral(rule.context, rule.symbol), total_result,
                                 evaluate=False)))
                    self.append(self.format_text("Therefore,"))
                    self.append(self.format_math_display(sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                                                                  _manualintegrate(rule),
                                                                  evaluate=False)))

    def print_Trig(self, rule):
        with self.new_step():
            text = {
                'sin': "The integral of sine is negative cosine:",
                'cos': "The integral of cosine is sine:",
                'sec*tan': "The integral of secant times tangent is secant:",
                'csc*cot': "The integral of cosecant times cotangent is cosecant:",
            }.get(rule.func)

            if text:
                self.append(self.format_text(text))

            self.append(self.format_math_display(sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                                                          _manualintegrate(rule),
                                                          evaluate=False)))

    def print_Exp(self, rule):
        with self.new_step():
            if rule.base == sympy.E:
                self.append(self.format_text("The integral of the exponential function is itself."))
            else:
                self.append(self.format_text("The integral of an exponential function is itself"
                                             " divided by the natural logarithm of the base."))
            self.append(self.format_math_display(sympy.Eq(sympy.Integral(rule.context, rule.symbol),
                                                          _manualintegrate(rule),
                                                          evaluate=False)))

    def print_simple(self, rule):
        with self.new_step():
            self.append(self.format_text("The integral of "),
                        self.format_math(rule.context),
                        self.format_text(" is "),
                        self.format_math(_manualintegrate(rule)))

    def print_Rewrite(self, rule):
        with self.new_step():
            self.append(self.format_text("Rewrite the integrand:"))
            self.append(self.format_math_display(sympy.Eq(rule.context, rule.rewritten, evaluate=False)))
            self.print_rule(rule.substep)

    def print_CompleteSquare(self, rule):
        with self.new_step():
            self.append(self.format_text("Complete the square:"))
            self.append(self.format_math_display(sympy.Eq(rule.context, rule.rewritten, evaluate=False)))
            self.print_rule(rule.substep)

    def print_DontKnow(self, rule):
        with self.new_step():
            self.append(self.format_text("Don't know the steps in finding this integral."))
            self.append(self.format_text("But the integral is"))
            self.append(self.format_math_display(sympy.integrate(rule.context, rule.symbol)))

    def print_Alternative(self, rule):
        # TODO: make more robust
        rule = filter_unknown_alternatives(rule)

        if len(rule.alternatives) == 1:
            self.print_rule(rule.alternatives[0])
            return

        if rule.context.func in self.alternative_functions_printed:
            self.print_rule(rule.alternatives[0])
        else:
            self.alternative_functions_printed.add(rule.context.func)
            with self.new_step():
                self.append(self.format_text("There are multiple ways to do this integral."))
                for index, r in enumerate(rule.alternatives):
                    with self.new_collapsible():
                        self.append_header("Method #{}".format(index + 1))
                        with self.new_level():
                            self.print_rule(r)

    def print_TrigSubstitution(self, rule):
        with self.new_step():
            d_x = DerivExpr(rule.symbol.name)
            d_theta = DerivExpr(rule.theta.name)
            deriv = sympy.diff(rule.func, rule.theta)
            self.append(self.format_text("Let "),
                        self.format_math(sympy.Eq(rule.symbol, rule.func, evaluate=False)),
                        self.format_text(', then '),
                        self.format_math(sympy.Eq(d_x, deriv*d_theta, evaluate=False)))
            self.append(self.format_text('Substitute:'))
            self.append(self.format_math_display(sympy.Integral(rule.substep.context, rule.substep.symbol)))
            with self.new_level():
                self.print_rule(rule.substep)

    def print_SqrtQuadratic(self, rule):
        a, b, c, x = rule.a, rule.b, rule.c, rule.symbol
        with self.new_step():
            self.append(self.format_text('Apply'))
            self.append(self.format_math_display(R'''\begin{align}
&\int\sqrt{a+bx+cx^2}\mathrm{d}x\\
=&x\sqrt{a+bx+cx^2}-\int x\mathrm{d}\sqrt{a+bx+cx^2}\\
=&x\sqrt{a+bx+cx^2}-\int\frac{x(b+2cx)}{2\sqrt{a+bx+cx^2}}\mathrm{d}x\\
=&x\sqrt{a+bx+cx^2}-\int\frac{2(a+bx+cx^2)-2a-bx}{2\sqrt{a+bx+cx^2}}\mathrm{d}x\\
=&x\sqrt{a+bx+cx^2}-\int\sqrt{a+bx+cx^2}\mathrm{d}x+\frac{1}{2}\int\frac{2a+bx}{\sqrt{a+bx+cx^2}}\mathrm{d}x\\
=&\frac{1}{2}x\sqrt{a+bx+cx^2}+\frac{1}{4}\int\frac{2a+bx}{\sqrt{a+bx+cx^2}}\mathrm{d}x
\end{align}'''))
            self.append(self.format_text('where '), self.format_math(f'a={a},b={b},c={c}'))
            integrand = (2*a+b*x)/sympy.sqrt(a+b*x+c*x**2)
            self.append(self.format_text('We then calculate '), self.format_math(sympy.Integral(integrand, x)))
            with self.new_level():
                substep = integral_steps(integrand, x)
                self.print_rule(substep)

    def print_SqrtQuadraticDenom(self, rule):
        a, b, c, coeffs, x = rule.a, rule.b, rule.c, rule.coeffs.copy(), rule.symbol
        N = len(rule.coeffs)
        integral = sympy.Add(*(coeff * sympy.Symbol(f'I_{i}') for coeff, i in zip(coeffs, range(N - 1, -1, -1))))
        result_coeffs = []
        for i in range(N-2):
            n = len(coeffs)-1-i
            coeff = coeffs[i]/(c*n)
            result_coeffs.append(coeff)
            coeffs[i+1] -= (2*n-1)*b/2*coeff
            coeffs[i+2] -= (n-1)*a*coeff
        d, e = coeffs[-1], coeffs[-2]
        s = sympy.sqrt(a+b*x+c*x**2)
        poly = sympy.Add(*(coeff * x**i for coeff, i in zip(result_coeffs, range(N - 2, 0, -1))))*s
        with self.new_step():
            self.append(self.format_text('Let '), self.format_math(R'I_n=\int\frac{x^n}{\sqrt{a+bx+cx^2}}\mathrm{d}x'),
                        self.format_text(' and '), self.format_math(R'J_n=\int x^n\sqrt{a+bx+cx^2}\mathrm{d}x'))
            self.append(self.format_math(R'\forall n,'))
            self.append(self.format_math_display(R'''\begin{align}
I_n&=\frac{1}{c}\int\frac{x^{n-2}(a+bx+cx^2)-ax^{n-2}-bx^{n-1}}{\sqrt{a+bx+cx^2}}\mathrm{d}x\\
&=\frac{1}{c}(\int x^{n-2}\sqrt{a+bx+cx^2}\mathrm{d}x-\int\frac{ax^{n-2}+bx^{n-1}}{\sqrt{a+bx+cx^2}}\mathrm{d}x)\\
&=\frac{1}{c}(J_{n-2}-aI_{n-2}-bI_{n-1})
\end{align}'''))
            self.append(self.format_math(R'\forall n\neq-1,'))
            self.append(self.format_math_display(R'''\begin{align}
J_n&=\frac{1}{n+1}\int\sqrt{a+bx+cx^2}\mathrm{d}x^{n+1}\\
&=\frac{1}{n+1}(x^{n+1}\sqrt{a+bx+cx^2}-\int\frac{x^{n+1}(b+2cx)}{2\sqrt{a+bx+cx^2}}\mathrm{d}x)\\
&=\frac{1}{n+1}(x^{n+1}\sqrt{a+bx+cx^2}-\frac{b}{2}I_{n+1}-cI_{n+2})
\end{align}'''))
            self.append(self.format_text('So '), self.format_math(R'\forall n\geq2,'))
            self.append(self.format_math_display(R'''\begin{align}
I_n&=\frac{1}{c}(\frac{1}{n-1}(x^{n-1}\sqrt{a+bx+cx^2}-\frac{b}{2}I_{n-1}-cI_n)-aI_{n-2}-bI_{n-1})\\
&=\frac{1}{c}(\frac{x^{n-1}}{n-1}\sqrt{a+bx+cx^2}-\frac{2n-1}{2(n-1)}bI_{n-1}-aI_{n-2})-\frac{1}{n-1}I_n\\
&=\frac{1}{cn}x^{n-1}\sqrt{a+bx+cx^2}-\frac{2n-1}{2n}\frac{b}{c}I_{n-1}-\frac{n-1}{n}\frac{a}{c}I_{n-2}\\
\end{align}'''))
            self.append(self.format_text('By iteration, the integral '), self.format_math(integral),
                        self.format_text(' equals '),
                        self.format_math(poly + e * sympy.Symbol('I_1') + d * sympy.Symbol('I_0')))
            integrand = (d+e*x)/s
            self.append(self.format_text('We then calculate '), self.format_math(sympy.Integral(integrand, x)))
            with self.new_level():
                substep = integral_steps(integrand, x)
                self.print_rule(substep)

    def format_math_constant(self, math):
        return self.format_math_display(latex(math) + R"+ \mathrm{C}")

    def finalize(self):
        rule = filter_unknown_alternatives(self.rule)
        result = _manualintegrate(rule)
        if result:
            simp = sympy.simplify(sympy.trigsimp(result))
            if simp != result:
                result = simp
                with self.new_step():
                    self.append(self.format_text("Now simplify:"))
                    self.append(self.format_math_display(simp))
            with self.new_step():
                self.append(self.format_text("Add the constant of integration:"))
                answer = self.format_math_constant(result)
                self.append(answer)
                answer = answer.copy()  # pyodide#2530
        else:
            answer = None
        return {
            'content': {'level': self.stack},
            'answer': answer
        }


def print_json_steps(function, symbol):
    rule = integral_steps(function, symbol)
    if isinstance(rule, DontKnowRule):
        raise ValueError("Cannot evaluate integral")
    a = IntegralPrinter(rule)
    return a.finalize()
