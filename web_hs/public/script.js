// 스마트폰 과의존 자가진단 + 정서 위험 점수 산출기

const questions = [
  "스마트폰이 없으면 불안하다고 느낀다.",
  "스마트폰이 학업/업무에 방해가 된다고 느낀다.",
  "충동적으로 스마트폰을 사용할 때가 많다.",
  "잠들기 직전까지 스마트폰을 손에 쥐고 있는 편이다.",
  "가족 또는 친구와 스마트폰 사용으로 갈등한 적이 있다."
];

let currentQuestion = 0;
let answers = [];

function showQuestion() {
  const questionEl = document.getElementById("question");
  questionEl.innerText = questions[currentQuestion];


const progress = Math.round((currentQuestion / questions.length) * 100);
  document.getElementById("progress-text").innerText = `${progress}%`;
  document.getElementById("progress-bar").style.width = `${progress}%`;
}

function answer(score) {
  answers.push(score);
  currentQuestion++;
  if (currentQuestion < questions.length) {
    showQuestion();
  } else {
    showResult();
  }
}

function showResult() {
  const total = answers.reduce((a, b) => a + b, 0);
  let level = "";
  if (total <= 10) level = "정상";
  else if (total <= 15) level = "주의";
  else level = "위험";

  document.getElementById("quiz-container").innerHTML = `
    <h3>정서불안 위험도: ${level}</h3>
    <p>총점: ${total}점 / ${questions.length * 4}점</p>
    <p>당신은 스마트폰 사용이 정서에 영향을 줄 수 있는 ${level} 단계에 있습니다.</p>
  `;
}

// HTML 로딩 후 첫 질문 표시
window.onload = function () {
  showQuestion();
};

function showTab(tabId) {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => tab.classList.remove('active'));

  const activeTab = document.getElementById(tabId);
  if (activeTab) activeTab.classList.add('active');

  const content = document.querySelector('.content');
  if (tabId === 'home') {
    content.classList.add('home-fullscreen');
  } else {
    content.classList.remove('home-fullscreen');
  }
}
