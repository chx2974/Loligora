const root = document.documentElement, $ = id => document.getElementById(id);
const bind = (id, numId, prop, unit, cb) => {
  const el = $(id), num = $(numId), min = +el.min, max = +el.max;
  let last = +el.value;
  const apply = v => { last = v; el.value = v; root.style.setProperty(prop, v + unit); if (cb) cb(v); };
  const clamp = v => Math.min(max, Math.max(min, Math.round(v)));
  el.addEventListener("input", () => { num.value = el.value; apply(+el.value); });
  num.addEventListener("input", () => { const v = Number(num.value);
    if (num.value.trim() !== "" && Number.isFinite(v) && v >= min && v <= max) apply(Math.round(v)); });
  const commit = () => { const v = Number(num.value); const o = num.value.trim() !== "" && Number.isFinite(v) ? clamp(v) : last;
    num.value = o; apply(o); };
  num.addEventListener("change", commit); num.addEventListener("blur", commit);
  num.addEventListener("keydown", e => {
    if (e.key === "Enter") commit();
    if ((e.key === "ArrowUp" || e.key === "ArrowDown") && e.shiftKey) { e.preventDefault();
      const o = clamp((Number(num.value) || last) + (e.key === "ArrowUp" ? 10 : -10)); num.value = o; apply(o); }
  });
  apply(last);
};
let weight = 400, data = [], openGlyph = null;
bind("w", "wn", "--w", "", v => { weight = v; updateAdv(); });
bind("s", "sn", "--size", "px");
$("it").addEventListener("change", e => root.style.setProperty("--fs", e.target.checked ? "italic" : "normal"));
$("lines").addEventListener("change", e => document.body.classList.toggle("lines", e.target.checked));
$("box").addEventListener("change", e => document.body.classList.toggle("box", e.target.checked));

const GROUPS = ["Uppercase", "Lowercase", "Figures", "Punctuation", "Symbols & currency", "Maths", "Accented uppercase",
  "Accented lowercase", "Marks", "Spaces", "Other / unencoded"];
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const hex = cp => cp == null ? "no code point" : "U+" + cp.toString(16).toUpperCase().padStart(4, "0");
const advAt = (g, w) => { const a = g.adv; // piecewise linear through 100 / 400 / 950
  if (w <= 400) return a[100] + (a[400] - a[100]) * (w - 100) / 300;
  return a[400] + (a[950] - a[400]) * (w - 400) / 550; };
const fmt = n => (Math.round(n * 10) / 10).toString();
const isMark = cp => cp != null && cp >= 0x300 && cp <= 0x36F;
const MET = [["base", 800], ["xh", 800 - 518], ["cap", 800 - 720], ["asc", 800 - 760], ["desc", 1000]];

function glyphSvg(g, big) {
  const a = advAt(g, weight), x0 = 500 - a / 2;
  let body, note = "";
  const feat = g.feature && !g.contextual;
  if (g.cp != null || feat) {
    const ch = g.cp != null ? String.fromCodePoint(g.cp) : String.fromCodePoint(g.via);
    const txt = (isMark(g.cp) ? " " : "") + ch;
    const style = feat ? ` style="font-feature-settings:'${g.feature}' 1"` : "";
    body = `<text x="${x0}" y="800"${style} xml:space="preserve">${esc(txt)}</text>`;
  } else {
    body = `<path class="st" transform="translate(${500 - g.adv[400] / 2} 800)" d="${g.path}"/>`;
    note = "static 400";
  }
  const lines = MET.map(([c, y]) => `<line class="m ${c}" x1="-100" x2="1100" y1="${y}" y2="${y}"/>`).join("");
  const sp = g.group === "Spaces" ? `<rect class="always" x="${x0}" y="300" width="${a}" height="500"/>` : "";
  return { note, svg: `<svg class="g" viewBox="0 -250 1000 1250" aria-hidden="true">` +
    `<rect class="adv" data-g="${esc(g.name)}" x="${x0}" y="-250" width="${a}" height="1250"/>${sp}${lines}${body}</svg>` };
}
function cellHtml(g, i) {
  const { svg, note } = glyphSvg(g);
  const how = g.feature ? `<div class="lab">${esc(g.feature)}${g.contextual ? " (contextual)" : ""}</div>` : "";
  return `<button class="cell cl" data-i="${i}" title="${esc(g.name)}"><div class="gl">${svg}</div>` +
    `<div class="lab"><b>${esc(g.name)}</b></div><div class="lab">${hex(g.cp)}</div>` +
    `<div class="lab">adv <span class="av" data-i="${i}">${fmt(advAt(g, weight))}</span></div>${how}` +
    (note ? `<div class="stat">${note}</div>` : "") + `</button>`;
}
function updateAdv() {
  if (!data.length) return;
  document.querySelectorAll(".av").forEach(el => { el.textContent = fmt(advAt(data[+el.dataset.i], weight)); });
  document.querySelectorAll(".cell").forEach(c => {
    const g = data[+c.dataset.i], a = advAt(g, weight), r = c.querySelector(".adv");
    r.setAttribute("x", 500 - a / 2); r.setAttribute("width", a);
    c.querySelectorAll("text").forEach(t => t.setAttribute("x", 500 - a / 2));
    const al = c.querySelector(".always"); if (al) { al.setAttribute("x", 500 - a / 2); al.setAttribute("width", a); }
  });
  if (openGlyph != null) showDetail(openGlyph);
}

function showDetail(i) {
  openGlyph = i;
  const g = data[i], { svg, note } = glyphSvg(g, true), c = g.cp;
  const digit = c != null && ((c >= 0x30 && c <= 0x39) || [0xB2, 0xB3, 0xB9, 0xBC, 0xBD, 0xBE].includes(c)) && g.adv[400] === 580 && g.adv[100] === 580;
  const rows = [100, 400, 950].map(w => `<tr><th>advance ${w}</th><td>${g.adv[w]}</td></tr>`).join("");
  $("dbody").innerHTML = `<h3>${esc(g.name)}</h3><div class="big cl">${svg.replace('class="g"', 'class="g big-svg"')}</div>` +
    `<table><tr><th>code point</th><td>${hex(c)}${c != null ? " &nbsp;" + esc(String.fromCodePoint(c)) : ""}</td></tr>` +
    `<tr><th>group</th><td>${esc(g.group)}</td></tr>${rows}` +
    `<tr><th>at ${weight}</th><td>${fmt(advAt(g, weight))}</td></tr>` +
    (g.feature ? `<tr><th>reached by</th><td>${esc(g.feature)}${g.contextual ? " (contextual, after a capital)" : " on " + esc(g.viaName)}</td></tr>` : "") +
    `</table>` + (digit ? `<p class="lab">Tabular figure: 580 units at every weight.</p>` : "") +
    (note ? `<p class="lab">Drawn from the outline (${note}); weight and italic do not apply.</p>` : "");
  const dlg = $("detail"); dlg.hidden = false;
  dlg.querySelectorAll(".m").forEach(l => l.style.display = "block");
  dlg.querySelectorAll(".adv").forEach(l => l.style.display = "block");
}
const closeDetail = () => { openGlyph = null; $("detail").hidden = true; };
$("close").addEventListener("click", closeDetail);
$("detail").addEventListener("click", e => { if (e.target === $("detail")) closeDetail(); });
document.addEventListener("keydown", e => { if (e.key === "Escape") closeDetail(); });

function matches(g, q) {
  if (!q) return true;
  q = q.trim(); if (!q) return true;
  const ql = q.toLowerCase();
  if (/^(u\+|0x)?[0-9a-f]{4,6}$/i.test(q) && g.cp != null && (hex(g.cp).slice(2).toLowerCase() === ql.replace(/^(u\+|0x)/, "").padStart(4, "0"))) return true;
  if (/^u\+/i.test(q)) return g.cp != null && hex(g.cp).toLowerCase().startsWith(ql);
  if ([...q].length === 1 && g.cp != null && String.fromCodePoint(g.cp) === q) return true;
  return g.name.toLowerCase().includes(ql);
}
function render() {
  const q = $("q").value;
  const by = {};
  data.forEach((g, i) => { if (matches(g, q)) (by[g.group] = by[g.group] || []).push(i); });
  Object.values(by).forEach(l => l.sort((a, b) => (data[a].cp ?? 1e9) - (data[b].cp ?? 1e9) || a - b));
  let total = 0;
  const html = GROUPS.filter(n => by[n]).map(n => { total += by[n].length;
    return `<section><h2>${esc(n)} <span class="n">(${by[n].length})</span></h2><div class="grid">` +
      by[n].map(i => cellHtml(data[i], i)).join("") + `</div></section>`; }).join("");
  $("table").innerHTML = html || `<p class="note">No glyph matches.</p>`;
  $("summary").textContent = q.trim() ? `${total} of ${data.length} glyphs match.` : `${data.length} glyphs in the font.`;
}
$("table").addEventListener("click", e => { const c = e.target.closest(".cell"); if (c) showDetail(+c.dataset.i); });
$("q").addEventListener("input", render);

if (location.protocol === "file:") { $("nofile").hidden = false; $("summary").textContent = ""; }
else fetch("glyphs.json").then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }).then(j => {
  data = j.glyphs; render();
}).catch(err => { $("summary").textContent = "Could not load glyphs.json (" + err.message + "). Run make build."; });
const ok = spec => document.fonts.load(spec).then(f => f.some(x => x.status === "loaded"), () => false);
if (location.protocol !== "file:") Promise.all([ok('16px "Loligora"'), ok('italic 16px "Loligora"')]).then(([up, it]) => {
  if (!up) $("nofont").hidden = false; else if (!it) $("noitalic").hidden = false;
});
