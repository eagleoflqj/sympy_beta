# SymPy Beta
SymPy Beta is a fork of [SymPy Gamma](https://github.com/sympy/sympy_gamma). The purpose of this project is to run a [SymPy](https://github.com/sympy/sympy)-powered, [Wolfram|Alpha](https://www.wolframalpha.com)-like answer engine totally in your browser, without backend computation.

SymPy Beta = SymPy Gamma + (Pyodide - GAE - django) + (Vue + NaiveUI - jQuery)

SymPy Beta is NOT an official SymPy project.
# Debug
```sh
npm i
npm run dev
```
Then open http://localhost:3000
# Run
```sh
npm i
npm run build
cd dist
python -m http.server
```
Then open http://localhost:8000
# License
AGPL 3.0 or later, with the exception of
* kernel/gamma derived from SymPy Gamma, which remains 3-clause BSD License from SymPy Gamma
* src/js/{factordiagram, plot}.js derived from SymPy Gamma, same above
