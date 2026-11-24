// Execute the actual compiled inline tag in a mock document; never sends HTTP.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const htmlFile = process.argv[2];
if (!htmlFile) throw new Error('Pass the newly built public/index.html');
const html = fs.readFileSync(htmlFile, 'utf8');
const match = html.match(/<script\b(?=[^>]*\bid\s*=\s*["']?site-analytics(?:["'\s>]))[^>]*>([\s\S]*?)<\/script>/i);
assert.ok(match, 'compiled production inline tag exists');
const cases = [
  ['http:', 'localhost', false],
  ['https:', 'localhost', false],
  ['http:', '127.0.0.1', false],
  ['https:', '[::1]', false],
  ['https:', 'preview.localhost', false],
  ['https:', 'preview.example.invalid', false],
  ['https:', 'docdrhabibcil.com.attacker.invalid', false],
  ['http:', 'docdrhabibcil.com', false],
  ['https:', 'docdrhabibcil.com', true],
  ['https:', 'www.docdrhabibcil.com', true],
];
const reports = [];
for (const [protocol, hostname, enabled] of cases) {
  const appended = [];
  const sandbox = {
    location: {protocol, hostname},
    document: {
      createElement(tag) {assert.equal(tag, 'script'); return {};},
      head: {appendChild(script) {appended.push(script);}},
    },
  };
  sandbox.window = sandbox;
  vm.runInNewContext(match[1], sandbox, {timeout:1000});
  assert.equal(appended.length, enabled ? 1 : 0, `${protocol}//${hostname}: loader count`);
  if (enabled) {
    assert.equal(appended[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-TDC4PMVEMK');
    assert.equal(appended[0].async, true);
    assert.equal(sandbox.dataLayer.length, 2);
    assert.equal(sandbox.dataLayer[1][0], 'config');
    assert.equal(sandbox.dataLayer[1][1], 'G-TDC4PMVEMK');
  } else {
    assert.equal(sandbox.dataLayer, undefined, 'preview has no measurement queue');
  }
  reports.push({protocol,hostname,enabled,pass:true});
}
console.log(JSON.stringify({scope:'Actual compiled inline script, VM/mock document only; no requests or real analytics events',htmlFile,passed:reports.length,cases:reports},null,2));
