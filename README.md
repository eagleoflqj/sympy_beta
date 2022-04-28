# SymPy Beta
![](https://img.shields.io/github/license/eagleoflqj/sympy_beta)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/eagleoflqj/sympy_beta.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/eagleoflqj/sympy_beta/alerts/)
[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/eagleoflqj/sympy_beta.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/eagleoflqj/sympy_beta/context:javascript)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/eagleoflqj/sympy_beta.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/eagleoflqj/sympy_beta/context:python)

Try me at https://sympy-beta.vercel.app!

SymPy Beta is a fork of [SymPy Gamma](https://github.com/sympy/sympy_gamma). The purpose of this project is to run a [SymPy](https://github.com/sympy/sympy)-powered, [Wolfram|Alpha](https://www.wolframalpha.com)-like answer engine totally in your browser, without backend computation.

Originally,  
SymPy Beta = SymPy Gamma + (Pyodide - GAE - django) + (Vue + NaiveUI - jQuery)

Since 0.5.0, the Pyodide Shell is added (and jQuery is back for using jQuery Terminal)

Since 0.6.0, extra functionalities are added to the kernel. See [kernel extension](kernel/extension)

SymPy Beta is NOT an official SymPy project.
# Document
See [doc](doc).
# License
AGPL 3.0 or later, with the exception of
* kernel/gamma derived from SymPy Gamma, which remains 3-clause BSD License from SymPy Gamma
* src/js/{factordiagram, plot}.js derived from SymPy Gamma, same above
* public/shell.js and src/views/Terminal.vue derived from Pyodide, which remain MPL-2.0
* kernel/extension/elementary/num2words.py derived from [num2words](https://github.com/savoirfairelinux/num2words), which switched from LGPL-2.1 to GPL-3.0-or-later in order to be compatible with AGPL
