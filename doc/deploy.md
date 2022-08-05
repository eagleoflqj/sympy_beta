# Deploy
SymPy Beta can be deployed to any HTTP server that hosts static files.

As long as you obey the AGPLv3+ license, you are free to host SymPy Beta w/o modification anywhere for any purpose.
## Generate assets
For deployment purpose, you don't need to install all Python packages inside `kernel/requirements.txt`. But you do need `build`, and all Node packages:
```sh
pip install build
npm i -g pnpm
pnpm i
```
Then run
```sh
pnpm run build
```
and everything you need is in `dist` directory.
## Serve
Now you can either run
```sh
python -m http.server -d dist
```
and open http://localhost:8000, or run
```sh
pnpm run serve
```
and open http://localhost:4173.
## Vercel
SymPy Beta is officially hosted on Vercel.

To achieve this, you should connect a git repo of SymPy Beta to a Vercel project.

As the server doesn't have `python` command available, and doesn't install `build` by default, you may also configure the `BUILD COMMAND` as
```sh
sed -i "s/'python'/'python3'/g" scripts/* && pip install build && npm run build
```
