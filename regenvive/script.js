// Replace with your RegenVive affiliate links (official order page) per package.
const CHECKOUT_LINKS = {
  2: "#",
  3: "#",
  6: "#",
};

document.documentElement.classList.add("js");

// Mobile menu
const toggle = document.querySelector(".nav-toggle");
const menu = document.getElementById("nav-menu");

function setMenu(open) {
  menu.classList.toggle("open", open);
  toggle.setAttribute("aria-expanded", String(open));
  toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
}

toggle.addEventListener("click", () => setMenu(!menu.classList.contains("open")));
menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });
window.matchMedia("(min-width: 861px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });

// Header shadow + back-to-top button
const header = document.querySelector(".site-header");
const toTop = document.querySelector(".to-top");
function onScroll() {
  const y = window.scrollY;
  header.classList.toggle("scrolled", y > 10);
  toTop.classList.toggle("show", y > 600);
}
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

// Reveal on scroll
const revealEls = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  revealEls.forEach((el) => io.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add("visible"));
}

// FAQ: keep only one answer open at a time
const faqItems = document.querySelectorAll(".faq details");
faqItems.forEach((d) => d.addEventListener("toggle", () => {
  if (d.open) faqItems.forEach((o) => { if (o !== d) o.open = false; });
}));

// Buy buttons
document.querySelectorAll(".js-buy").forEach((btn) => {
  const url = CHECKOUT_LINKS[btn.dataset.package];
  if (url && url !== "#") {
    btn.href = url;
  } else {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      alert("Checkout link not set yet — add it in script.js (CHECKOUT_LINKS).");
    });
  }
});

document.getElementById("year").textContent = new Date().getFullYear();
