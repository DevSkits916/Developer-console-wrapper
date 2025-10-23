# Developer Console Wrapper

A single-page web app that simulates a lightweight browser. Enter a URL to load the
page in an iframe, inspect the fetched source, and run JavaScript commands in a
console—perfect for static hosting platforms like GitHub Pages or Render Static Sites.

## Features

- **URL Wrapper** – Load any embeddable page inside an iframe with minimal controls.
- **View Source** – Fetch the requested URL and display its HTML (subject to CORS).
- **Developer Console** – Execute JavaScript against the iframe's `window` context
  when same-origin rules allow it.
- **Keyboard Shortcut** – Use <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>Enter</kbd> to run
  console commands quickly.

## Usage

1. Deploy the contents of this repository to a static host (GitHub Pages, Render Static
   Sites, Netlify, etc.).
2. Visit the deployed URL and enter the address you want to inspect.
3. Click **Load Page** to navigate the iframe.
4. Use **View Source** to fetch the HTML markup. Some sites may block the request via
   CORS; when that happens the app explains the issue.
5. Type JavaScript into the developer console and press **Run** (or the keyboard
   shortcut). The output log records results and errors.

## Limitations

- Many modern sites prevent embedding or cross-origin access. For those, the iframe may
  remain blank, source requests can fail, and console commands will be blocked by the
  browser for security reasons.
- The console executes code via `eval` inside the iframe. Only use it on pages you
  trust.

## Local Preview

Open `index.html` directly in your browser or use a static server:

```bash
python -m http.server 4173
```

Then visit <http://localhost:4173/>.
