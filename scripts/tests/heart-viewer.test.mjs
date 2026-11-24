import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

const source = await fs.readFile(new URL('../../assets/js/heart-viewer.js', import.meta.url), 'utf8');
const { createHeartRenderLoop, initViewer } = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const results = [];
function check(name, run) { run(); results.push({ name, status: 'PASS' }); }

let visible = false, animated = true, draws = 0, next = 0;
const frames = new Map();
const loop = createHeartRenderLoop({
  render: () => { draws += 1; }, shouldRender: () => visible, shouldAnimate: () => animated,
  requestFrame: (callback) => { const id = ++next; frames.set(id, callback); return id; },
  cancelFrame: (id) => frames.delete(id),
});
check('Offscreen initial state draws nothing and schedules no RAF', () => {
  loop.sync(); assert.equal(draws, 0); assert.equal(frames.size, 0);
});
check('Repeated visible updates keep one frame chain', () => {
  visible = true;
  for (let i = 0; i < 10; i++) loop.sync();
  assert.equal(frames.size, 1);
  const [id, callback] = frames.entries().next().value;
  frames.delete(id); callback();
  assert.equal(frames.size, 1);
});
check('Leaving viewport or hiding tab cancels outstanding RAF', () => {
  const before = draws;
  visible = false; loop.sync();
  assert.equal(frames.size, 0); assert.equal(draws, before);
});
check('Re-entry resumes only one frame chain', () => {
  visible = true; loop.sync(); loop.sync(); assert.equal(frames.size, 1);
});
check('Reduced motion or pause renders one still frame without a loop', () => {
  animated = false; const before = draws; loop.sync();
  assert.equal(draws, before + 1); assert.equal(frames.size, 0);
});
check('Disposal prevents re-entry from restarting frames', () => {
  loop.dispose(); animated = true; const before = draws; loop.sync();
  assert.equal(draws, before); assert.equal(frames.size, 0);
});

class Target {
  events = new Map();
  addEventListener(name, handler) {
    if (!this.events.has(name)) this.events.set(name, new Set());
    this.events.get(name).add(handler);
  }
  removeEventListener(name, handler) { this.events.get(name)?.delete(handler); }
  async emit(name, event = {}) { for (const handler of [...(this.events.get(name) || [])]) await handler(event); }
}
class Element extends Target {
  hidden = false; disabled = false; dataset = {}; attrs = new Map(); textContent = ''; isConnected = true;
  setAttribute(name, value) { this.attrs.set(name, value); }
  removeAttribute(name) { this.attrs.delete(name); }
  getAttribute(name) { return this.attrs.get(name); }
  getBoundingClientRect() { return { top: 0, bottom: 400, left: 0, right: 300 }; }
}
const elements = Object.fromEntries(['viewer', 'poster', 'status', 'load', 'motion', 'hint'].map((name) => [name, new Element()]));
const root = new Element();
root.dataset = { loadingLabel: 'Loading', errorLabel: 'An illustration remains available.', retryLabel: 'Retry' };
root.querySelector = (selector) => elements[selector.match(/data-heart-(\w+)/)?.[1]];
const preference = new Target(); preference.matches = false;
const fakeWindow = new Target();
Object.assign(fakeWindow, { innerHeight: 900, innerWidth: 1280, matchMedia: () => preference });
const fakeDocument = new Target();
let probes = 0;
Object.assign(fakeDocument, { hidden: false, querySelectorAll: () => [], createElement: () => { probes++; return { getContext: () => null }; } });
globalThis.window = fakeWindow;
globalThis.document = fakeDocument;
check('Viewer startup and duplicate bootstrap do not request WebGL or a model', () => {
  initViewer(root); initViewer(root);
  assert.equal(root.dataset.heartState, 'idle');
  assert.equal(elements.load.hidden, false);
  assert.equal(probes, 0);
  assert.equal(elements.load.events.get('click').size, 1);
});
const oldWarn = console.warn; console.warn = () => {};
try {
  await elements.load.emit('click');
  check('WebGL unavailable fails before remote imports, retains poster and Retry', () => {
    assert.equal(probes, 1);
    assert.equal(root.dataset.heartState, 'error');
    assert.equal(elements.poster.hidden, false);
    assert.equal(elements.load.hidden, false);
    assert.equal(elements.load.disabled, false);
    assert.equal(elements.load.textContent, 'Retry');
    assert.equal(elements.status.textContent, 'An illustration remains available.');
  });
  await elements.load.emit('click');
  check('Retry after unavailable WebGL remains a recoverable state', () => {
    assert.equal(probes, 2); assert.equal(elements.load.disabled, false);
    assert.equal(root.dataset.heartState, 'error');
  });
} finally { console.warn = oldWarn; delete globalThis.window; delete globalThis.document; }
console.log(JSON.stringify({ type: 'Node lifecycle and DOM-stub regression; not browser/WebGL/CPU timing', tests: results, passed: results.length }, null, 2));
