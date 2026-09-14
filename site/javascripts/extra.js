document.addEventListener("DOMContentLoaded", () => {
  const search = document.querySelector(".md-search");
  const input = document.querySelector(".md-search__input");

  if (!search || !input) return;

  // Show/hide "Press /"
  const updateHint = () => {
    search.classList.toggle(
      "search-active",
      input.value.length > 0 || document.activeElement === input
    );
  };

  input.addEventListener("focus", updateHint);
  input.addEventListener("input", updateHint);
  input.addEventListener("blur", updateHint);

  // Clear search when clicking outside the search overlay
  search.addEventListener("click", (event) => {
    if (event.target.classList.contains("md-search__overlay")) {
      input.value = "";
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }
  });

  // Clear search when navigating to another page
  document.addEventListener("click", (event) => {
    const link = event.target.closest("a");

    if (link && link.href && link.href !== window.location.href) {
      input.value = "";
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }
  });
});