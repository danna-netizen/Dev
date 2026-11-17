// Dami Soporte: comportamiento mínimo (copiar, contador, estado de envío)
document.addEventListener("click", async (e) => {
  const btn = e.target.closest("[data-copy]");
  if (!btn) return;
  const text = btn.dataset.copy;
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const range = document.createRange();
    const node = btn.closest(".mailbox")?.querySelector(".mailbox__addr");
    if (node) { range.selectNodeContents(node); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(range); document.execCommand("copy"); }
  }
  btn.setAttribute("data-copied", "");
  btn.setAttribute("aria-label", "Correo copiado");
  clearTimeout(btn._t);
  btn._t = setTimeout(() => { btn.removeAttribute("data-copied"); btn.removeAttribute("aria-label"); }, 2000);
});

document.querySelectorAll("form[data-busy]").forEach((form) => {
  form.addEventListener("submit", () => {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) { btn.setAttribute("aria-busy", "true"); setTimeout(() => (btn.disabled = true), 0); }
  });
});

document.querySelectorAll("textarea[data-count]").forEach((ta) => {
  const out = document.getElementById(ta.dataset.count);
  const max = ta.maxLength;
  const update = () => { out.textContent = `${ta.value.length.toLocaleString("es")} / ${max.toLocaleString("es")}`; };
  ta.addEventListener("input", update);
  update();
});

// Aviso de prioridad alta: se muestra al elegir "Alta"
document.querySelectorAll('input[name="priority"]').forEach((radio) => {
  radio.addEventListener("change", () => {
    const notice = document.querySelector("[data-high-priority]");
    if (notice) notice.hidden = document.querySelector('input[name="priority"]:checked')?.value !== "alta";
  });
});
