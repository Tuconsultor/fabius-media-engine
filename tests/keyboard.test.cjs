const assert = require('node:assert/strict');
const fs = require('node:fs');
const {test} = require('node:test');
const vm = require('node:vm');

const source = fs.readFileSync('src/fabius_media_engine/static/app.js', 'utf8');

function mount() {
  const ids = ['media-url', 'status', 'result', 'normalize', 'inspect', 'download-video',
               'download-audio', 'download-images'];
  const elements = Object.fromEntries(ids.map(id => [id, {
    disabled: false, value: '', listeners: {}, classList: {toggle() {}},
    addEventListener(type, listener) { this.listeners[type] = listener; },
    click() { if (!this.disabled) this.listeners.click?.(); },
    focus() {},
  }]));
  const calls = [];
  vm.runInNewContext(source, {
    document: {
      getElementById: id => elements[id],
      querySelectorAll: () => ids.slice(3).map(id => elements[id]),
    },
    fetch: (path, request) => {
      calls.push([path, JSON.parse(request.body)]);
      return new Promise(() => {});
    },
  });
  elements['media-url'].value = 'https://x.com/i/status/123';
  return {input: elements['media-url'], calls};
}

test('Enter in the URL field normalizes once while busy', () => {
  const {input, calls} = mount();
  const event = {key: 'Enter', preventDefault() {}};
  input.listeners.keydown?.(event);
  input.listeners.keydown?.(event);
  assert.deepEqual(calls, [['/api/normalize', {url: 'https://x.com/i/status/123'}]]);
});

test('accepting an input-method composition does not send a request', () => {
  const {input, calls} = mount();
  input.listeners.keydown?.({key: 'Enter', isComposing: true, preventDefault() {}});
  assert.deepEqual(calls, []);
});
