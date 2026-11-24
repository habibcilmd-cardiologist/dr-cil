// Search is progressively enhanced; input and index content are rendered as text.
(function () {
  "use strict";
  var wrapper = document.getElementById("search-wrapper");
  var modal = document.getElementById("search-modal");
  var input = document.getElementById("search-query");
  var output = document.getElementById("search-results");
  var status = document.getElementById("search-status");
  var hideButton = document.getElementById("close-search-button");
  if (!wrapper || !modal || !input || !output || !status || !hideButton) return;

  var fuse;
  var indexed = false;
  var indexing = false;
  var indexError = false;
  var visible = false;
  var releaseDialog = null;

  function message(key) { return wrapper.getAttribute("data-" + key) || ""; }
  function showMessage(text) {
    output.replaceChildren();
    status.textContent = text;
  }
  function links() { return Array.from(output.querySelectorAll("a[href]")); }

  function displaySearch(event) {
    if (!window.drcilDialog || visible) return;
    wrapper.hidden = false;
    visible = true;
    releaseDialog = window.drcilDialog.activate(modal, {
      opener: event && event.currentTarget ? event.currentTarget : document.activeElement,
      initialFocus: input,
      onClose: hideSearch
    });
    if (!indexed && !indexing) buildIndex();
    else if (indexing) showMessage(message("loading"));
  }
  function hideSearch() {
    if (!visible) return;
    visible = false;
    wrapper.hidden = true;
    input.value = "";
    output.replaceChildren();
    status.textContent = "";
    if (releaseDialog) releaseDialog();
    releaseDialog = null;
  }

  ["search-button", "search-button-mobile"].forEach(function (id) {
    document.getElementById(id)?.addEventListener("click", displaySearch);
  });
  hideButton.addEventListener("click", hideSearch);
  wrapper.addEventListener("click", function (event) { if (event.target === wrapper) hideSearch(); });
  input.form?.addEventListener("submit", function (event) { event.preventDefault(); });
  input.addEventListener("input", function () { executeQuery(input.value); });

  document.addEventListener("keydown", function (event) {
    var active = document.activeElement;
    if (event.key === "/" && !visible && !window.drcilDialog?.isOpen() &&
        !active.matches("input, textarea, select") && !active.isContentEditable) {
      event.preventDefault();
      displaySearch();
    }
    if (!visible) return;
    if (event.key === "Escape") { event.preventDefault(); hideSearch(); return; }
    var results = links();
    var index = results.indexOf(active);
    if (event.key === "ArrowDown" && results.length && (active === input || index >= 0)) {
      event.preventDefault();
      results[Math.min(index + 1, results.length - 1)].focus();
    } else if (event.key === "ArrowUp" && (active === input || index >= 0)) {
      event.preventDefault();
      (index <= 0 ? input : results[index - 1]).focus();
    } else if (event.key === "Enter" && active === input) {
      event.preventDefault();
      if (results.length) results[0].focus();
    }
  });

  function buildIndex() {
    indexing = true;
    indexError = false;
    output.setAttribute("aria-busy", "true");
    showMessage(message("loading"));
    var request = new XMLHttpRequest();
    function fail() {
      indexing = false;
      indexError = true;
      indexed = false;
      fuse = undefined;
      output.setAttribute("aria-busy", "false");
      if (visible) showMessage(message("error"));
    }
    request.onload = function () {
      if (request.status !== 200) { fail(); return; }
      try {
        var data = JSON.parse(request.responseText);
        if (!Array.isArray(data) || typeof Fuse !== "function") throw new Error("Invalid search index");
        fuse = new Fuse(data, {
          shouldSort: true, ignoreLocation: true, threshold: 0.0, includeMatches: true,
          keys: [{ name: "title", weight: 0.8 }, { name: "section", weight: 0.2 },
            { name: "summary", weight: 0.6 }, { name: "content", weight: 0.4 }]
        });
        indexing = false;
        indexed = true;
        output.setAttribute("aria-busy", "false");
        if (visible) executeQuery(input.value);
      } catch (error) { fail(); }
    };
    request.onerror = fail;
    request.ontimeout = fail;
    request.onabort = fail;
    request.open("GET", wrapper.getAttribute("data-url").replace(/\/?$/, "/") + "index.json");
    request.timeout = 15000;
    request.send();
  }

  function plain(value) {
    var decoder = document.createElement("textarea");
    decoder.innerHTML = String(value || "").replace(/<[^>]*>/g, "");
    return decoder.value;
  }
  function textElement(tag, className, text) {
    var node = document.createElement(tag);
    node.className = className;
    node.textContent = text;
    return node;
  }
  function executeQuery(term) {
    if (!fuse) { showMessage(message(indexError ? "error" : "loading")); return; }
    if (!term.trim()) { showMessage(""); return; }
    var results = fuse.search(term);
    if (!results.length) { showMessage(message("empty").replace("{query}", term)); return; }
    var fragment = document.createDocumentFragment();
    results.forEach(function (result) {
      var item = result.item;
      var target;
      try { target = new URL(item.externalUrl || item.permalink, location.href); }
      catch (error) { return; }
      if (!/^https?:$/.test(target.protocol)) return;
      var row = document.createElement("li");
      row.className = "mb-2";
      var link = document.createElement("a");
      link.className = "block px-3 py-2 rounded-md bg-neutral-100 dark:bg-neutral-700 hover:bg-primary-100 dark:hover:bg-primary-900";
      link.href = target.href;
      if (item.externalUrl) { link.target = "_blank"; link.rel = "noopener noreferrer"; }
      link.appendChild(textElement("div", "text-lg font-bold", plain(item.title)));
      var metadata = [plain(item.section), item.date || ""].filter(Boolean).join(" · ");
      var language = item.language || (/^\/en\//.test(target.pathname) ? "en" : /^\/ar\//.test(target.pathname) ? "ar" : "tr");
      link.lang = language;
      link.dir = language === "ar" ? "rtl" : "ltr";
      if (language !== document.documentElement.lang.split("-")[0]) metadata += " · " + (item.languageName || language.toUpperCase());
      link.appendChild(textElement("div", "text-sm text-neutral-500 dark:text-neutral-400", metadata));
      link.appendChild(textElement("div", "text-sm", plain(item.summary)));
      row.appendChild(link);
      fragment.appendChild(row);
    });
    output.replaceChildren(fragment);
    status.textContent = message("count").replace("{count}", String(output.children.length));
  }
})();
