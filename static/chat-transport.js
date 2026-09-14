// Reconnect with the same request ID, including after a stream is interrupted.
// Only validated answers are emitted; progress events keep the connection active.
async function readChatStream(response, onStatus) {
  if (!response.ok) {
    const result = await response.json();
    throw new Error(typeof result.detail === "string" ? result.detail : "Please check your message and try again.");
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  try {
    while (true) {
      const { value, done } = await reader.read();
      buffer += decoder.decode(value, { stream: !done });
      let boundary;
      while ((boundary = buffer.indexOf("\n\n")) !== -1) {
        const frame = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 2);
        const type = frame.split("\n").find((line) => line.startsWith("event: "))?.slice(7);
        const data = frame.split("\n").filter((line) => line.startsWith("data: ")).map((line) => line.slice(6)).join("\n");
        if (!data) continue;
        const payload = JSON.parse(data);
        if (type === "status") onStatus(payload.stage);
        if (type === "error") throw new Error(payload.detail);
        if (type === "result") return payload;
      }
      if (done) throw new TypeError("The connection was interrupted. Please try again.");
    }
  } finally {
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}

async function requestChat(body, signal, onStatus, fetcher = fetch) {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const response = await fetcher("/api/chat/stream", {
        method: "POST", headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
        signal, body,
      });
      return await readChatStream(response, onStatus);
    } catch (error) {
      if (!(error instanceof TypeError) || signal.aborted || attempt === 2) throw error;
      onStatus("reconnecting");
      await new Promise((resolve) => setTimeout(resolve, 500 * (attempt + 1)));
    }
  }
}

if (typeof module !== "undefined") module.exports = { readChatStream, requestChat };
