// Local override: shared modal behavior and progressively enhanced mobile navigation.
(function () {
  "use strict";

  var session = null;
  var focusableSelector = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), summary, [tabindex]:not([tabindex="-1"])';

  function focusable(panel) {
    return Array.from(panel.querySelectorAll(focusableSelector)).filter(function (element) {
      return element.getClientRects().length && !element.closest('[inert], [hidden]');
    });
  }

  function activate(panel, options) {
    if (session) session.requestClose();
    var opener = options.opener || document.activeElement;
    var overflow = document.body.style.overflow;
    var inertElements = [];
    var branch = panel;

    // Inert siblings along the ancestor path; never inert an ancestor of the dialog.
    while (branch.parentElement) {
      Array.from(branch.parentElement.children).forEach(function (sibling) {
        if (sibling !== branch && !/^(SCRIPT|STYLE|LINK)$/.test(sibling.tagName)) {
          inertElements.push({ element: sibling, wasInert: sibling.inert });
          sibling.inert = true;
        }
      });
      if (branch.parentElement === document.body) break;
      branch = branch.parentElement;
    }

    var current = { panel: panel, requestClose: options.onClose };
    session = current;
    document.body.style.overflow = "hidden";
    (options.initialFocus || focusable(panel)[0] || panel).focus({ preventScroll: true });

    return function release() {
      if (session !== current) return;
      session = null;
      inertElements.forEach(function (entry) { entry.element.inert = entry.wasInert; });
      document.body.style.overflow = overflow;
      if (opener && opener.isConnected) opener.focus({ preventScroll: true });
    };
  }

  document.addEventListener("keydown", function (event) {
    if (!session) return;
    if (event.key === "Escape") {
      event.preventDefault();
      event.stopImmediatePropagation();
      session.requestClose();
    } else if (event.key === "Tab") {
      var elements = focusable(session.panel);
      var first = elements[0] || session.panel;
      var last = elements[elements.length - 1] || session.panel;
      if (!elements.length || !session.panel.contains(document.activeElement) ||
          (event.shiftKey && (document.activeElement === first || document.activeElement === session.panel))) {
        event.preventDefault();
        (event.shiftKey ? last : first).focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  }, true);

  document.addEventListener("focusin", function (event) {
    if (session && !session.panel.contains(event.target)) {
      (focusable(session.panel)[0] || session.panel).focus({ preventScroll: true });
    }
  });

  window.drcilDialog = { activate: activate, isOpen: function () { return Boolean(session); } };

  var openButton = document.getElementById("menu-button");
  var closeButton = document.getElementById("menu-close-button");
  var wrapper = document.getElementById("menu-wrapper");
  var releaseMenu = null;

  function closeMenu() {
    if (!wrapper || wrapper.hidden) return;
    wrapper.hidden = true;
    openButton.setAttribute("aria-expanded", "false");
    if (releaseMenu) releaseMenu();
    releaseMenu = null;
  }

  if (openButton && closeButton && wrapper) {
    openButton.addEventListener("click", function () {
      if (!wrapper.hidden) { closeMenu(); return; }
      wrapper.hidden = false;
      openButton.setAttribute("aria-expanded", "true");
      releaseMenu = activate(wrapper, { opener: openButton, initialFocus: closeButton, onClose: closeMenu });
    });
    closeButton.addEventListener("click", closeMenu);
    wrapper.addEventListener("click", function (event) {
      if (event.target === wrapper || event.target.closest("a[href]")) closeMenu();
    });
    window.addEventListener("pagehide", closeMenu);
    var desktop = window.matchMedia("(min-width: 1024px)");
    if (desktop.addEventListener) desktop.addEventListener("change", function (event) { if (event.matches) closeMenu(); });
  }

  // These native controls work without the bundle too; enhancement adds dismissal.
  document.addEventListener("click", function (event) {
    document.querySelectorAll(".drcil-language-switcher[open], .drcil-fallback-navigation[open]").forEach(function (details) {
      if (!details.contains(event.target)) details.open = false;
    });
  });
  document.addEventListener("keydown", function (event) {
    var details = event.target.closest(".drcil-language-switcher[open], .drcil-fallback-navigation[open]");
    if (event.key === "Escape" && details) {
      event.preventDefault();
      details.open = false;
      details.querySelector("summary").focus();
    }
  });

  document.documentElement.classList.add("drcil-interactive");
  var header = document.querySelector(".drcil-fixed-header");
  if (header) {
    var sizeHeader = function () {
      document.documentElement.style.setProperty("--drcil-header-height", Math.ceil(header.getBoundingClientRect().height) + "px");
    };
    sizeHeader();
    if ("ResizeObserver" in window) new ResizeObserver(sizeHeader).observe(header);
    else window.addEventListener("resize", sizeHeader);
  }
})();
