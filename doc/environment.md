# Prepare Environment
SymPy Beta can be developed on Linux, macOS and Windows, with 100% Open Source tools.

Software|Version|Reason|Ubuntu|macOS|Windows x64|Windows arm64
-|-|-|-|-|-|-
Python|3.10|Pyodide 0.20.0|conda|conda|choco|WSL
Node|>=14|Vercel|nvm|nvm|choco|[Unoffical build](https://unofficial-builds.nodejs.org/download/release/v17.5.0/)
VSCodium|latest|-|Ubuntu Software|brew|choco|[GitHub Release](https://github.com/VSCodium/vscodium/releases)
PyCharm CE|latest|-|Ubuntu Software|brew|choco|-

* Make sure `python` and `pip` commands are in your `PATH` and point to correct version.
* PyCharm CE is optional. If you use it, you may open `kernel` directory with it.

You may need the following VSCodium extensions:
- Python
- Pyright
- Vue Language Features

# Install packages
```sh
npm i  # rerun after dependencies in package.json change
pip install -r kernel/requirements.txt  # rerun after kernel/requirements.txt changes
node scripts/download_vocabulary.mjs  # no need to rerun in near future
node scripts/build_antlr.mjs  # no need to rerun, this is subject to change after sympy upgrades antlr dependency
node scripts/build_wheel.mjs  # rerun after kernel changes (frequently)
```
