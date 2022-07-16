# Run locally
```sh
npm run dev
```
Then open http://localhost:5173/.

> **_NOTE:_** This doesn't work if you want to test PWA.
You should "[deploy](deploy.md)" it locally.

Hot-reload works for UI changes,
but sometimes you have to refresh to make sure it's in a clean state.

If you change kernel, you have to re-generate kernel wheel and refresh.

# Directory walk through
SymPy Beta is an SPA, and [index.html](../index.html) is that single page.
Except for some CDN imports that should be replaced in the future, it references [main.js](../src/main.js) to provide functionalities.
## src
[src](../src) contains front end code.

The structure doesn't need explaining if you have basic knowledge of Vue,
except for, [components/contents](../src/components/contents) contains dynamic components that are loaded by [BetaContainer](../src/components/BetaContainer.vue) according to what kind of card is shown,
while [components](../src/components) contains static components.
## kernel
[kernel](../kernel) contains kernel code.

New code should be covered 100% in [test](../kernel/test), with the exception of `Exception`.
## scripts
[scripts](../scripts) contains cross-platform node scripts for maintaining purpose.
