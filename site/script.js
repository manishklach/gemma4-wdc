document.querySelectorAll('a[href$=".md"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    if (window.location.protocol === "file:") {
      event.preventDefault();
    }
  });
});

