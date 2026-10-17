"use strict";

// Progressive enhancement only: every project remains visible without JS.
const projects = Array.from(document.querySelectorAll(".project-card[data-category]"));
const filters = Array.from(document.querySelectorAll(".filter[data-filter]"));
const countElement = document.getElementById("project-count");
const compactGrid = document.querySelector(".project-small-grid");

function setFilter(filter) {
  if (!["all", "ai", "web", "experimental"].includes(filter)) return;

  let shown = 0;
  projects.forEach((project) => {
    const visible = filter === "all" || project.dataset.category === filter;
    project.hidden = !visible;
    if (visible) shown += 1;
  });

  filters.forEach((button) => {
    const selected = button.dataset.filter === filter;
    button.classList.toggle("active", selected);
    button.setAttribute("aria-pressed", String(selected));
  });

  if (compactGrid) {
    compactGrid.hidden = !Array.from(
      compactGrid.querySelectorAll(".project-card[data-category]")
    ).some((project) => !project.hidden);
  }

  if (countElement) countElement.textContent = String(shown).padStart(2, "0");
}

filters.forEach((button) =>
  button.addEventListener("click", () => setFilter(button.dataset.filter))
);

const menuButton = document.querySelector(".menu-toggle");
const menu = document.getElementById("primary-nav");

function closeMenu() {
  if (!menu || !menuButton) return;
  menu.classList.remove("is-open");
  menuButton.setAttribute("aria-expanded", "false");
}

if (menu && menuButton) {
  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") === "true";
    menu.classList.toggle("is-open", !open);
    menuButton.setAttribute("aria-expanded", String(!open));
  });

  menu.querySelectorAll("a").forEach((link) =>
    link.addEventListener("click", closeMenu)
  );

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  window.matchMedia("(min-width: 591px)").addEventListener("change", (event) => {
    if (event.matches) closeMenu();
  });
}

const year = document.getElementById("year");
if (year) year.textContent = String(new Date().getFullYear());
