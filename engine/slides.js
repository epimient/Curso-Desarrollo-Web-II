(function () {
  const slides = Array.from(document.querySelectorAll("[data-slide]"));
  if (!slides.length) return;

  const prevBtn = document.getElementById("prev");
  const nextBtn = document.getElementById("next");
  const counter = document.getElementById("counter");
  const dots = document.getElementById("dots");

  let current = 0;

  function update() {
    slides.forEach((s, i) => s.classList.toggle("is-active", i === current));

    if (prevBtn) prevBtn.disabled = current === 0;
    if (nextBtn) nextBtn.disabled = current === slides.length - 1;
    if (counter) counter.textContent = `${current + 1} / ${slides.length}`;

    if (dots) {
      const dotEls = dots.querySelectorAll(".dot");
      dotEls.forEach((d, i) => d.classList.toggle("is-active", i === current));
    }
  }

  function go(n) {
    current = Math.max(0, Math.min(current + n, slides.length - 1));
    update();
  }

  function goTo(n) {
    current = Math.max(0, Math.min(n, slides.length - 1));
    update();
  }

  if (prevBtn) prevBtn.addEventListener("click", () => go(-1));
  if (nextBtn) nextBtn.addEventListener("click", () => go(1));

  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") go(-1);
    if (e.key === "ArrowRight" || e.key === " ") {
      e.preventDefault();
      go(1);
    }
  });

  let touchStartX = 0;
  document.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
  });
  document.addEventListener("touchend", (e) => {
    const diff = touchStartX - e.changedTouches[0].screenX;
    if (Math.abs(diff) > 50) go(diff > 0 ? 1 : -1);
  });

  if (dots) {
    slides.forEach((_, i) => {
      const dot = document.createElement("span");
      dot.className = "dot" + (i === 0 ? " is-active" : "");
      dot.addEventListener("click", () => goTo(i));
      dots.appendChild(dot);
    });
  }

  update();
})();
