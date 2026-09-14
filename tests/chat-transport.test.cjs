const { test } = require("node:test");
const assert = require("node:assert/strict");
const { readChatStream, requestChat } = require("../static/chat-transport.js");

function stream(text) {
  const bytes = new TextEncoder().encode(text);
  return new Response(new ReadableStream({start(controller) {
    // Split every byte, including Arabic UTF-8 and SSE frame boundaries.
    for (const byte of bytes) controller.enqueue(Uint8Array.of(byte));
    controller.close();
  }}));
}

test("decodes fragmented Arabic events without showing partial drafts", async () => {
  const stages = [];
  const result = await readChatStream(stream('event: status\ndata: {"stage":"checking"}\n\nevent: result\ndata: {"answer":"أهلاً"}\n\n'), stage => stages.push(stage));
  assert.deepEqual(stages, ["checking"]);
  assert.equal(result.answer, "أهلاً");
});

test("interrupted stream reconnects with the identical body and yields one result", async () => {
  const bodies = [], stages = [];
  const body = JSON.stringify({request_id:"same-id", question:"hello"});
  const result = await requestChat(body, new AbortController().signal, stage => stages.push(stage), async (_, options) => {
    bodies.push(options.body);
    return stream(bodies.length === 1 ? 'event: status\ndata: {"stage":"answering"}\n\n' : 'event: result\ndata: {"answer":"done"}\n\n');
  });
  assert.deepEqual(bodies, [body, body]);
  assert.ok(stages.includes("reconnecting"));
  assert.equal(result.answer, "done");
});

test("model errors are surfaced once instead of retrying inference", async () => {
  let calls = 0;
  await assert.rejects(requestChat("{}", new AbortController().signal, () => {}, async () => {
    calls++;
    return stream('event: error\ndata: {"detail":"Model unavailable","status":503}\n\n');
  }), /Model unavailable/);
  assert.equal(calls, 1);
});

test("HTTP overload errors and aborted requests do not reconnect", async () => {
  let calls = 0;
  await assert.rejects(requestChat("{}", new AbortController().signal, () => {}, async () => {
    calls++;
    return new Response('{"detail":"Queue full"}', {status:429});
  }), /Queue full/);
  const controller = new AbortController();
  controller.abort();
  await assert.rejects(requestChat("{}", controller.signal, () => {}, async () => {
    calls++;
    throw new TypeError("Failed to fetch");
  }), /Failed to fetch/);
  assert.equal(calls, 2);
});
