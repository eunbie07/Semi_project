let isScrolling = false;

function smoothScrollTo(targetY, duration = 1400) {
  const startY = window.scrollY;
  const distance = targetY - startY;
  const startTime = performance.now();

  function animate(currenttime) {
    const elapsed = currenttime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const ease = easeInOutCubic(progress);

    window.scrollTo(0, startY + distance * ease);

    if (progress < 1) {
      requestAnimationFrame(animate);
    } 
  }

  requestAnimationFrame(animate);
}

function easeInOutCubic(t) {
    return t < 0.5
    ? 4 * t * t * t
    : 1 - Math.pow(1 - t, 6);
  }

window.addEventListener("wheel", (e) => {
  if (isScrolling) return;

  e.preventDefault(); // 기본 휠 스크롤 막음
  isScrolling = true;

  const direction = e.deltaY > 0 ? 1 : -1;
  const sections = document.querySelectorAll(".full-section");
  const currentIndex = Math.round(window.scrollY / window.innerHeight);
  const nextIndex = currentIndex + direction;

  if (nextIndex >= 0 && nextIndex < sections.length) {
    const targetY = sections[nextIndex].offsetTop;
    smoothScrollTo(targetY, 1200); // ⏱ 원하는 속도로 조절 가능
  } else {
    isScrolling = false;
  }
}, { passive: false });
