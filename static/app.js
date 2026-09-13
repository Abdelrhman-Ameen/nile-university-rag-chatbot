// A small chat UI. Model output is rendered as text, never as HTML.
const $ = (selector) => document.querySelector(selector);
let turns = [],
  savedChats = [],
  currentChat = null,
  library = [],
  busy = false;
let statusTimer;
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function dateLabel(value) {
  return new Date(value).toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}
function sourceLink(source, text) {
  const link = el("a", "", text);
  try {
    const url = new URL(source.url);
    if (["https:", "http:"].includes(url.protocol)) {
      if (source.page) url.hash = `page=${source.page}`;
      link.href = url.href;
    }
  } catch {
    link.href = "#";
  }
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  return link;
}
function toast(text) {
  $("#toast").textContent = text;
  $("#toast").hidden = false;
  setTimeout(() => {
    $("#toast").hidden = true;
  }, 2200);
}
function error(text) {
  $("#error").textContent = text;
  $("#error").hidden = !text;
}
function scrollChat() {
  $("#conversation").scrollTop = $("#conversation").scrollHeight;
}
function message(role, text = "") {
  const wrapper = el("article", `message ${role}`);
  if (role === "assistant") {
    const label = el("div", "assistant-label");
    const circle = el("span", "assistant-logo");
    const logo = el("img");
    logo.src = "/static/nu-logo.png";
    logo.alt = "";
    circle.append(logo);
    label.append(circle, el("span", "", "Nile University"));
    wrapper.append(label);
  }
  const body = el("div", "message-text", text);
  body.dir = "auto";
  wrapper.append(body);
  $("#messages").append(wrapper);
  return wrapper;
}
function renderAnswer(result) {
  const wrapper = message("assistant");
  const body = wrapper.querySelector(".message-text");
  for (const paragraph of result.answer.split(/\n\s*\n/)) {
    const p = el("p");
    p.dir = "auto";
    for (const part of paragraph.split(/(\[\d+\]|\*\*[^*\n]+\*\*)/g)) {
      const match = /^\[(\d+)\]$/.exec(part);
      const source =
        match && result.sources.find((s) => s.citation === Number(match[1]));
      if (source) {
        const link = sourceLink(source, part);
        link.className = "citation";
        link.title = source.title;
        p.append(link);
      } else if (part.startsWith("**") && part.endsWith("**"))
        p.append(el("strong", "", part.slice(2, -2)));
      else p.append(document.createTextNode(part));
    }
    body.append(p);
  }
  const actions = el("div", "message-actions");
  const copy = el("button", "copy-button", "Copy");
  copy.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(result.answer);
      toast("Copied");
    } catch {
      toast("Select the text to copy.");
    }
  });
  actions.append(copy);
  wrapper.append(actions);
  const citedSources = result.sources.filter((s) => s.cited);
  if (citedSources.length) {
    const details = el("details", "answer-sources");
    details.append(el("summary", "", "Sources"));
    for (const source of citedSources) {
      const card = el("div", "source-card");
      card.append(sourceLink(source, `[${source.citation}] ${source.title}`));
      card.append(
        el(
          "small",
          "",
          `${source.kind.toUpperCase()}${source.page ? ` · p. ${source.page}` : ""} · ${dateLabel(source.fetched_at)}`,
        ),
      );
      const quote = el("blockquote", "", source.text);
      quote.dir = "auto";
      card.append(quote);
      details.append(card);
    }
    wrapper.append(details);
  }
}
function renderRecent() {
  $("#recent-chats").replaceChildren();
  savedChats.forEach((chat) => {
    const button = el(
      "button",
      currentChat === chat ? "selected" : "",
      chat.title,
    );
    button.disabled = busy;
    button.addEventListener("click", () => {
      if (busy) return;
      currentChat = chat;
      turns = [...chat.turns];
      $("#messages").replaceChildren();
      $("#chat-panel").classList.remove("empty");
      turns.forEach((turn) =>
        turn.role === "user"
          ? message("user", turn.content)
          : renderAnswer(turn.result),
      );
      renderRecent();
      closeSidebar();
      error("");
      scrollChat();
    });
    $("#recent-chats").append(button);
  });
}
function closeSidebar() {
  $("#sidebar").classList.remove("open");
  $("#menu-button").setAttribute("aria-expanded", "false");
}
function resetChat() {
  if (busy) return;
  currentChat = null;
  turns = [];
  $("#messages").replaceChildren();
  $("#chat-panel").classList.add("empty");
  $("#question").value = "";
  error("");
  renderRecent();
  closeSidebar();
  $("#question").focus();
}
async function sendQuestion(question) {
  if (busy || !question.trim()) return;
  busy = true;
  error("");
  closeSidebar();
  $("#chat-panel").classList.remove("empty");
  $("#send-button").disabled = true;
  $("#new-chat").disabled = true;
  renderRecent();
  const user = message("user", question);
  $("#question").value = "";
  const loading = message("assistant");
  const indicator = el("div", "loading-text");
  indicator.append(el("span", "spinner"), el("span", "", "Thinking…"));
  loading.querySelector(".message-text").append(indicator);
  scrollChat();
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: AbortSignal.timeout(240000),
      body: JSON.stringify({
        question,
        language: $("#reply-language").value,
        history: turns
          .slice(-6)
          .map((t) => ({ role: t.role, content: t.content.slice(0, 5000) })),
      }),
    });
    const result = await response.json();
    if (!response.ok)
      throw new Error(
        typeof result.detail === "string"
          ? result.detail
          : "Please shorten your message and try again.",
      );
    loading.remove();
    renderAnswer(result);
    turns.push(
      { role: "user", content: question },
      { role: "assistant", content: result.answer, result },
    );
    if (!currentChat) {
      currentChat = { title: question, turns: [] };
      savedChats.unshift(currentChat);
    }
    currentChat.turns = [...turns];
  } catch (err) {
    loading.remove();
    user.remove();
    $("#question").value = question;
    error(
      err.name === "TimeoutError"
        ? "Qwen took too long. Please try again."
        : err.message === "Failed to fetch"
          ? "The server is unavailable. Please restart it."
          : err.message,
    );
    if (!turns.length) $("#chat-panel").classList.add("empty");
  } finally {
    busy = false;
    $("#send-button").disabled = false;
    $("#new-chat").disabled = false;
    renderRecent();
    scrollChat();
    $("#question").focus();
    loadStatus();
  }
}
$("#chat-form").addEventListener("submit", (e) => {
  e.preventDefault();
  sendQuestion($("#question").value.trim());
});
$("#question").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
    e.preventDefault();
    if (!busy) $("#chat-form").requestSubmit();
  }
});
$("#new-chat").addEventListener("click", resetChat);
$("#menu-button").addEventListener("click", () => {
  const open = $("#sidebar").classList.toggle("open");
  $("#menu-button").setAttribute("aria-expanded", String(open));
});
$("main").addEventListener("click", (event) => {
  if (!event.target.closest("#menu-button")) closeSidebar();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeSidebar();
});
function renderLibrary() {
  const query = $("#source-search").value.toLowerCase();
  const matches = library.filter((s) =>
    `${s.title} ${s.url}`.toLowerCase().includes(query),
  );
  $("#library-results").replaceChildren();
  if (!matches.length)
    $("#library-results").append(el("p", "", "No sources found."));
  matches.forEach((source) => {
    const row = el("article", "library-row");
    row.append(
      el("span", "tag", source.kind.toUpperCase()),
      sourceLink(source, source.title),
    );
    row.append(
      el("small", "", `${source.url} · ${dateLabel(source.fetched_at)}`),
    );
    $("#library-results").append(row);
  });
}
async function openLibrary() {
  closeSidebar();
  $("#library-dialog").showModal();
  $("#library-results").textContent = "Loading…";
  try {
    const response = await fetch("/api/sources");
    if (!response.ok) throw new Error("Sources unavailable.");
    library = (await response.json()).sources;
    renderLibrary();
  } catch (err) {
    $("#library-results").textContent = err.message;
  }
}
$("#library-button").addEventListener("click", openLibrary);
$("#close-library").addEventListener("click", () =>
  $("#library-dialog").close(),
);
$("#source-search").addEventListener("input", renderLibrary);
$("#status-button").addEventListener("click", loadStatus);
async function loadStatus() {
  clearTimeout(statusTimer);
  try {
    const response = await fetch("/api/health");
    if (!response.ok) throw new Error();
    const status = await response.json();
    $("#status-dot").classList.toggle(
      "pending",
      !status.model_ready || !status.index_ready,
    );
    $("#status-text").textContent = status.model_ready
      ? "Qwen 3"
      : "Qwen offline";
    $("#status-button").title = status.model_ready
      ? "Qwen is ready"
      : "Click to check Qwen";
    $("#notice").hidden = status.model_ready && status.index_ready;
    $("#notice").textContent = !status.index_ready
      ? "Sources are not indexed yet."
      : "Qwen is not ready yet. Please wait for the model to finish loading.";
    if (!status.model_ready || !status.index_ready)
      statusTimer = setTimeout(loadStatus, 10000);
  } catch {
    $("#status-dot").classList.add("pending");
    $("#status-text").textContent = "Offline";
  }
}
loadStatus();
