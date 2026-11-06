#!/usr/bin/env node
/* kaggle-competitions — desktop pane.
   Live submission board for tracked competitions: best score, recent runs,
   pending alerts. Polls the dashboard API endpoint served by this plugin. */
(function () {
  "use strict";

  const API = "/api/plugins/kaggle-competitions/submissions";
  const REFRESH_MS = 120000;

  function el(html) {
    const d = document.createElement("div");
    d.innerHTML = html.trim();
    return d.firstChild;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, c => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"
    }[c]));
  }

  function render(container, data) {
    const comps = Object.keys(data || {});
    if (!comps.length) {
      container.innerHTML = '<div class="kc-empty">No competitions tracked yet.<br>Set plugin settings → competitions.</div>';
      return;
    }
    container.innerHTML = comps.map(c => {
      const d = data[c] || {};
      if (d.error) return `<div class="kc-comp"><div class="kc-name">${esc(c)}</div><div class="kc-err">${esc(d.error)}</div></div>`;
      const rows = (d.recent || []).slice(0, 5).map(r =>
        `<div class="kc-row"><span class="kc-score">${esc(r.score || "—")}</span><span class="kc-desc">${esc(r.desc || r.status)}</span></div>`
      ).join("");
      const best = d.best != null ? d.best : "—";
      return `<div class="kc-comp">
        <div class="kc-head"><span class="kc-name">${esc(c)}</span><span class="kc-best">best <b>${esc(best)}</b></span></div>
        ${rows}
      </div>`;
    }).join("");
  }

  function tick(container) {
    fetch(API, { credentials: "include" })
      .then(r => (r.ok ? r.json() : Promise.reject(r.status)))
      .then(data => render(container, data))
      .catch(() => { container.innerHTML = '<div class="kc-empty">kaggle API unreachable (auth?)</div>'; });
  }

  function init() {
    const container = el('<div class="kaggle-competitions-pane"><div class="kc-title">kaggle · live board</div><div class="kc-body">loading…</div></div>');
    const body = container.querySelector(".kc-body");
    try { Hermes.registerPane({ id: "kaggle-competitions", title: "Kaggle", el: container }); }
    catch (e) { /* pane API shape drift — fall back to console */ console.warn("pane register failed", e); }
    tick(body);
    setInterval(() => tick(body), REFRESH_MS);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
