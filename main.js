const urlInput = document.getElementById('url-input');
const loadBtn = document.getElementById('load-btn');
const viewSourceBtn = document.getElementById('view-source-btn');
const closeSourceBtn = document.getElementById('close-source-btn');
const sourcePanel = document.getElementById('source-panel');
const sourceOutput = document.getElementById('source-output');
const iframe = document.getElementById('page-frame');
const consoleInput = document.getElementById('console-input');
const runConsoleBtn = document.getElementById('run-console-btn');
const consoleOutput = document.getElementById('console-output');

const DEFAULT_URL = 'https://example.com/';

function normalizeUrl(rawValue) {
  try {
    if (!rawValue) {
      return DEFAULT_URL;
    }

    const hasScheme = /^(https?:)?\/\//i.test(rawValue.trim());
    const value = hasScheme ? rawValue.trim() : `https://${rawValue.trim()}`;
    return new URL(value).href;
  } catch (error) {
    return null;
  }
}

function appendConsoleLine(type, value) {
  const line = document.createElement('div');
  line.className = `console-line${type === 'error' ? ' error' : ''}`;

  const prefix = document.createElement('strong');
  prefix.textContent = type === 'error' ? 'Error:' : 'Result:';

  const content = document.createElement('span');
  content.textContent = typeof value === 'string' ? value : JSON.stringify(value);

  line.append(prefix, content);
  consoleOutput.appendChild(line);
  consoleOutput.scrollTop = consoleOutput.scrollHeight;
}

function loadPage() {
  const normalized = normalizeUrl(urlInput.value);
  if (!normalized) {
    appendConsoleLine('error', 'Invalid URL.');
    return;
  }

  iframe.src = normalized;
  hideSourcePanel();
  appendConsoleLine('result', `Navigated to ${normalized}`);
}

async function fetchSource() {
  const normalized = normalizeUrl(urlInput.value);
  if (!normalized) {
    appendConsoleLine('error', 'Enter a valid URL before fetching source.');
    return;
  }

  try {
    const response = await fetch(normalized, {
      mode: 'cors',
      credentials: 'omit',
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const text = await response.text();
    sourceOutput.textContent = text;
    showSourcePanel();
    appendConsoleLine('result', `Fetched source for ${normalized}`);
  } catch (error) {
    sourceOutput.textContent = String(error);
    showSourcePanel(true);
    appendConsoleLine(
      'error',
      'Unable to fetch source. The site may block cross-origin requests or embedding.'
    );
  }
}

function showSourcePanel(isError = false) {
  sourcePanel.hidden = false;
  viewSourceBtn.setAttribute('aria-expanded', 'true');
  if (isError) {
    sourcePanel.classList.add('has-error');
  } else {
    sourcePanel.classList.remove('has-error');
  }
}

function hideSourcePanel() {
  sourcePanel.hidden = true;
  viewSourceBtn.setAttribute('aria-expanded', 'false');
}

function runConsoleCommand() {
  const code = consoleInput.value;
  if (!code.trim()) {
    return;
  }

  try {
    const frameWindow = iframe.contentWindow;
    if (!frameWindow) {
      throw new Error('No frame content available yet. Load a page first.');
    }

    const result = frameWindow.eval(code);
    appendConsoleLine('result', result);
  } catch (error) {
    const message =
      error instanceof DOMException
        ? 'Cannot run code in this page because of cross-origin restrictions.'
        : error.message || String(error);
    appendConsoleLine('error', message);
  }
}

function setup() {
  urlInput.value = DEFAULT_URL;
  iframe.src = DEFAULT_URL;

  loadBtn.addEventListener('click', loadPage);
  viewSourceBtn.addEventListener('click', fetchSource);
  closeSourceBtn.addEventListener('click', hideSourcePanel);
  runConsoleBtn.addEventListener('click', runConsoleCommand);

  consoleInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && (event.metaKey || event.ctrlKey)) {
      event.preventDefault();
      runConsoleCommand();
    }
  });
}

document.addEventListener('DOMContentLoaded', setup);
