const questions = [
  "요즘 들어 이유 없이 슬프거나 허무함을 느끼나요?",
  "하루 일과에 집중하기 힘들고 무기력한 편인가요?",
  "수면 패턴이 평소와 다르거나 불면을 겪고 있나요?",
  "사람들과의 관계에서 거리감을 느끼고 외로움을 느끼나요?",
  "스마트폰을 쓸 때 마음이 더 복잡해지는 느낌이 있나요?"
];

let currentIndex = 0;
let totalScore = 0;

function answer(score) {
  totalScore += score;
  currentIndex++;

  if (currentIndex < questions.length) {
    updateQuiz();
  } else {
    showResult();
  }
}

function updateQuiz() {
  const questionEl = document.getElementById("question");
  const progressText = document.getElementById("progress-text");
  const progressBar = document.getElementById("progress-bar");

  if (questionEl && progressText && progressBar) {
    questionEl.textContent = questions[currentIndex];
    const percent = Math.round((currentIndex / questions.length) * 100);
    progressText.textContent = `${percent}% 완료`;
    progressBar.style.width = `${percent}%`;
  }
}

function showResult() {
  const questionEl = document.getElementById("question");
  const buttons = document.querySelectorAll(".quiz-btn");
  const progressText = document.getElementById("progress-text");
  const progressBar = document.getElementById("progress-bar");
  const progressWrapper = document.getElementById("progress-wrapper");
  const resultEl = document.getElementById("result");

  if (questionEl) questionEl.style.display = "none";
  buttons.forEach(btn => btn.style.display = "none");
  if (progressText) progressText.style.display = "none";
  if (progressBar) progressBar.style.display = "none";
  if (progressWrapper) progressWrapper.style.display = "none";

  let message = "";
  if (totalScore >= 17) {
    message = "⚠️ 정서적으로 위험할 수 있어요. 전문가 상담을 고려해보세요.";
  } else if (totalScore >= 12) {
    message = "😟 약간의 정서적 불안이 느껴지네요. 스스로 돌보는 시간을 가져보세요.";
  } else {
    message = "😊 현재 상태는 비교적 안정적이에요. 좋은 습관을 유지하세요!";
  }

  resultEl.innerHTML = `<strong>결과:</strong> ${message}`;
}

// 초기 로딩 시 첫 질문 세팅
window.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("question")) {
    updateQuiz();
  }
});
