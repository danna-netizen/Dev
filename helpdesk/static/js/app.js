(function () {
  // Kanban: drag a card to another column to change its stage.
  var csrf = document.body.dataset.csrf;
  var dragged = null;

  function updateCounts() {
    document.querySelectorAll(".column").forEach(function (col) {
      var n = col.querySelectorAll(".card").length;
      col.querySelector(".count").textContent = n;
      var empty = col.querySelector(".col-empty");
      if (n === 0 && !empty) {
        var p = document.createElement("p");
        p.className = "col-empty";
        p.textContent = "No tickets";
        col.querySelector(".cards").appendChild(p);
      } else if (n > 0 && empty) {
        empty.remove();
      }
    });
  }

  document.querySelectorAll(".card[draggable]").forEach(function (card) {
    card.addEventListener("dragstart", function (e) {
      dragged = card;
      card.classList.add("dragging");
      e.dataTransfer.effectAllowed = "move";
      e.dataTransfer.setData("text/plain", card.dataset.id);
    });
    card.addEventListener("dragend", function () {
      card.classList.remove("dragging");
      document.querySelectorAll(".drop-target").forEach(function (c) { c.classList.remove("drop-target"); });
    });
  });

  document.querySelectorAll(".column").forEach(function (col) {
    col.addEventListener("dragover", function (e) {
      if (!dragged) return;
      e.preventDefault();
      col.classList.add("drop-target");
    });
    col.addEventListener("dragleave", function (e) {
      if (!col.contains(e.relatedTarget)) col.classList.remove("drop-target");
    });
    col.addEventListener("drop", function (e) {
      e.preventDefault();
      col.classList.remove("drop-target");
      if (!dragged) return;
      var card = dragged;
      dragged = null;
      var from = card.closest(".column");
      if (from === col) return;
      var body = new URLSearchParams({ stage: col.dataset.stage });
      col.querySelector(".cards").prepend(card);
      updateCounts();
      fetch("/helpdesk/tickets/" + card.dataset.id + "/stage", {
        method: "POST",
        headers: { "X-CSRF-Token": csrf, "X-Requested-With": "fetch", "Content-Type": "application/x-www-form-urlencoded" },
        body: body,
        credentials: "same-origin"
      }).then(function (r) {
        if (!r.ok) throw new Error("failed");
      }).catch(function () {
        from.querySelector(".cards").prepend(card);
        updateCounts();
        alert("Could not move the ticket. Please try again.");
      });
    });
  });

  // Scroll the conversation to the latest message after sending.
  if (location.hash === "#chatter-end") {
    var end = document.getElementById("chatter-end");
    if (end) end.scrollIntoView({ block: "center" });
  }
})();

// Admin: show / hide demo passwords.
(function () {
  function toggle(btn, show) {
    var s = btn.parentElement.querySelector(".secret");
    if (!s) return;
    s.textContent = show ? s.dataset.secret : "••••••••";
    btn.textContent = show ? "Hide" : "Show";
  }
  document.querySelectorAll("[data-reveal]").forEach(function (btn) {
    btn.addEventListener("click", function () { toggle(btn, btn.textContent === "Show"); });
  });
  var all = document.querySelector("[data-reveal-all]");
  if (all) all.addEventListener("click", function () {
    var show = all.textContent.indexOf("Show") === 0;
    document.querySelectorAll("[data-reveal]").forEach(function (b) { toggle(b, show); });
    all.textContent = show ? "Hide all passwords" : "Show all passwords";
  });
})();
