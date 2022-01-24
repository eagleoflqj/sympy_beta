const categorys = [
  {
    name: 'Arithmetic',
    sub_categorys: [
      {
        name: 'Fractions',
        examples: [
          { name: 'Simplify fractions', expression: '242/33' },
          { name: 'Rationalize repeating decimals', expression: '0.[123]' }
        ]
      },
      {
        name: 'Approximations',
        examples: [
          { name: null, expression: 'pi' },
          { name: null, expression: 'E' },
          { name: null, expression: 'exp(pi)' }
        ]
      }
    ]
  },
  {
    name: 'Algebra',
    sub_categorys: [
      {
        name: null,
        examples: [
          { name: null, expression: 'x' },
          { name: null, expression: '(x+2)/((x+3)*(x-4))' },
          { name: null, expression: 'simplify((x**2 - 4)/((x+3)*(x-2)))' }
        ]
      },
      {
        name: 'Polynomial and Rational Functions',
        examples: [
          { name: 'Polynomial division', expression: 'div(x**2 - 4 + x, x-2)' },
          { name: 'Greatest common divisor', expression: 'gcd(2*x**2 + 6*x, 12*x)' },
          { name: '&hellip;and least common multiple', expression: 'lcm(2*x**2 + 6*x, 12*x)', html: true },
          { name: 'Factorization', expression: 'factor(x**4/2 + 5*x**3/12 - x**2/3)' },
          { name: 'Multivariate factorization', expression: 'factor(x**2 + 4*x*y + 4*y**2)' },
          { name: 'Symbolic roots', expression: 'solve(x**2 + 4*x*y + 4*y**2)' },
          { name: null, expression: 'solve(x**2 + 4*x*y + 4*y**2, y)' },
          { name: 'Complex roots', expression: 'solve(x**2 + 4*x + 181, x)' },
          { name: 'Irrational roots', expression: 'solve(x**3 + 4*x + 181, x)' },
          { name: 'Systems of equations', expression: 'solve_poly_system([y**2 - x**3 + 1, y*x], x, y)' }
        ]
      }
    ]
  },
  {
    name: 'Trigonometry',
    sub_categorys: [
      {
        name: null,
        examples: [
          { name: null, expression: 'sin(2*x)' },
          { name: null, expression: 'tan(1 + x)' }
        ]
      }
    ]
  },
  {
    name: 'Calculus',
    sub_categorys: [
      {
        name: 'Limits',
        examples: [
          { name: null, expression: 'limit(tan(x), x, pi/2)' },
          { name: null, expression: 'limit(tan(x), x, pi/2, dir="-")' }
        ]
      },
      {
        name: 'Derivatives',
        examples: [
          { name: 'Derive the product rule', expression: 'diff(f(x)*g(x)*h(x))' },
          { name: '&hellip;as well as the quotient rule', expression: 'diff(f(x)/g(x))', html: true },
          { name: 'Get steps for derivatives', expression: 'diff((sin(x) * x^2) / (1 + tan(cot(x))))' },
          { name: 'Multiple ways to derive functions', expression: 'diff(cot(x*y), y)' },
          { name: 'Implicit derivatives, too', expression: 'diff(y(x)^2 - 5*sin(x), x)' }
        ]
      },
      {
        name: 'Integrals',
        examples: [
          { name: null, expression: 'integrate(tan(x))' },
          { name: 'Multiple variables', expression: 'integrate(2*x + y, y)' },
          { name: 'Limits of integration', expression: 'integrate(2*x + y, (x, 1, 3))' },
          { name: null, expression: 'integrate(2*x + y, (x, 1, 3), (y, 2, 4))' },
          { name: 'Improper integrals', expression: 'integrate(tan(x), (x, 0, pi/2))' },
          { name: 'Exact answers', expression: 'integrate(1/(x**2 + 1), (x, 0, oo))' },
          { name: 'Get steps for integrals', expression: 'integrate(exp(x)/(1 + exp(2*x)))' },
          { name: null, expression: 'integrate(1/((x+1)*(x+3)*(x+5)))' },
          { name: null, expression: 'integrate((2*x + 3)**7)' }
        ]
      },
      {
        name: 'Series',
        examples: [
          { name: null, expression: 'series(sin(x), x, pi/2)' }
        ]
      }
    ]
  },
  {
    name: 'Number Theory',
    sub_categorys: [
      {
        name: null,
        examples: [
          { name: null, expression: '1006!' },
          { name: null, expression: '10!!' },
          { name: null, expression: 'factorint(12321)' },
          { name: 'Calculate the 42<sup>nd</sup> prime', expression: 'prime(42)', html: true },
          { name: 'Calculate ϕ(x), the Euler totient function', expression: 'totient(42)' },
          { name: null, expression: 'isprime(12321)' },
          { name: 'First prime greater than 42', expression: 'nextprime(42)' }
        ]
      },
      {
        name: 'Diophantine Equations',
        examples: [
          { name: null, expression: 'diophantine(x**2 - 4*x*y + 8*y**2 - 3*x + 7*y - 5)' },
          { name: null, expression: 'diophantine(2*x + 3*y - 5)' },
          { name: null, expression: 'diophantine(3*x**2 + 4*y**2 - 5*z**2 + 4*x*y - 7*y*z + 7*z*x)' }
        ]
      }
    ]
  },
  {
    name: 'Discrete Mathematics',
    sub_categorys: [
      {
        name: 'Boolean Logic',
        examples: [
          { name: null, expression: '(x | y) & (x | ~y) & (~x | y)' },
          { name: null, expression: 'x & ~x' }
        ]
      },
      {
        name: 'Recurrences',
        examples: [
          { name: 'Solve a recurrence relation', expression: 'rsolve(y(n+2)-y(n+1)-y(n), y(n))' },
          { name: 'Specify initial conditions', expression: 'rsolve(y(n+2)-y(n+1)-y(n), y(n), {y(0): 0, y(1): 1})' }
        ]
      },
      {
        name: 'Summation',
        examples: [
          { name: null, expression: 'Sum(k, (k, 1, m))' },
          { name: null, expression: 'Sum(x**k, (k, 0, oo))' },
          { name: null, expression: 'Product(k**2, (k, 1, m))' },
          { name: null, expression: 'summation(1/2**i, (i, 0, oo))' },
          { name: null, expression: 'product(i, (i, 1, k), (k, 1, n))' }
        ]
      }
    ]
  },
  {
    name: 'Plotting',
    sub_categorys: [
      {
        name: null,
        examples: [
          { name: null, expression: 'plot(sin(x) + cos(2*x))' },
          { name: 'Multiple plots', expression: 'plot([x, x^2, x^3, x^4])' },
          { name: 'Polar plots', expression: 'plot(r=1-sin(theta))' },
          { name: 'Parametric plots', expression: 'plot(x=cos(t), y=sin(t))' },
          { name: 'Multiple plot types', expression: 'plot(y=x, y1=x^2, r=cos(theta), r1=sin(theta))' }
        ]
      }
    ]
  },
  {
    name: 'Miscellaneous',
    sub_categorys: [
      {
        name: null,
        examples: [
          { name: 'Documentation for functions', expression: 'factorial2' },
          { name: null, expression: 'sympify' },
          { name: null, expression: 'bernoulli' }
        ]
      }
    ]
  }
]

export default categorys
