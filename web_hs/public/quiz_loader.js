document.addEventListener("DOMContentLoaded", () => {
    fetch("quiz_menu.html")
      .then(res => res.text())
      .then(html => {
        document.getElementById("quiz").innerHTML = html;
      });
  });
  
  function loadQuiz(page) {
    fetch(page)
      .then(res => res.text())
      .then(html => {
        document.getElementById("quiz").innerHTML = html;
        window.scrollTo({
          top: document.getElementById("quiz").offsetTop,
          behavior: "smooth"
        });
      });
  }
  