# SymPy Beta
![](https://img.shields.io/github/license/eagleoflqj/sympy_beta)

Try me at https://sympy-beta.vercel.app!

SymPy Beta is a fork of [SymPy Gamma](https://github.com/sympy/sympy_gamma). The purpose of this project is to run a [SymPy](https://github.com/sympy/sympy)-powered, [Wolfram|Alpha](https://www.wolframalpha.com)-like answer engine totally in your browser, without backend computation.

Originally,  
SymPy Beta = SymPy Gamma + (Pyodide - GAE - django) + (Vue + NaiveUI - jQuery)

But as development continues,
it goes [far beyond](doc/changelog.md) SymPy **Gamma**,
although still needs to learn much from the respected model Wolfram|**Alpha**.

That's why I name it SymPy **Beta**.

SymPy Beta is **NOT** an official SymPy project.
# Document
See [doc](doc).
# License
AGPL 3.0 or later, with the exception of
* kernel/gamma derived from SymPy Gamma, which remains 3-clause BSD License from SymPy Gamma
* src/js/{factordiagram, plot}.js derived from SymPy Gamma, same above
* public/shell.js and src/views/Terminal.vue derived from Pyodide, which remain MPL-2.0
* kernel/extension/elementary/num2words.py derived from [num2words](https://github.com/savoirfairelinux/num2words), which switched from LGPL-2.1 to GPL-3.0-or-later in order to be compatible with AGPL
