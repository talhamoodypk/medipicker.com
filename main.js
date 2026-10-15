const chips = document.querySelectorAll(".chip");
const blocks = document.querySelectorAll(".cat-block");
const products = document.querySelectorAll(".product");
const search = document.getElementById("q");
const noResults = document.querySelector(".no-results");
let activeCat = "all";

function apply() {
  const q = search.value.trim().toLowerCase();
  let shown = 0;
  blocks.forEach((block) => {
    const inCat = activeCat === "all" || block.dataset.catBlock === activeCat;
    let visible = 0;
    block.querySelectorAll(".product").forEach((p) => {
      const match = inCat && (!q || p.dataset.name.includes(q));
      p.hidden = !match;
      if (match) visible++;
    });
    block.hidden = visible === 0;
    shown += visible;
  });
  noResults.hidden = shown !== 0;
}

chips.forEach((chip) => chip.addEventListener("click", () => {
  activeCat = chip.dataset.filter;
  chips.forEach((c) => {
    const on = c === chip;
    c.classList.toggle("is-active", on);
    c.setAttribute("aria-pressed", String(on));
  });
  apply();
}));

search.addEventListener("input", () => {
  if (search.value && activeCat !== "all") {
    activeCat = "all";
    chips.forEach((c) => {
      const on = c.dataset.filter === "all";
      c.classList.toggle("is-active", on);
      c.setAttribute("aria-pressed", String(on));
    });
  }
  apply();
  if (search.value.trim()) document.getElementById("products").scrollIntoView({ block: "start" });
});

const toTop = document.querySelector(".to-top");
window.addEventListener("scroll", () => toTop.classList.toggle("show", window.scrollY > 600), { passive: true });

document.getElementById("year").textContent = new Date().getFullYear();
