function initQuizMenu() {
  const quiz1Btn = document.getElementById("quiz1");
  const quiz2Btn = document.getElementById("quiz2");
  if (quiz1Btn) quiz1Btn.onclick = () => loadQuiz1();
  if (quiz2Btn) quiz2Btn.onclick = () => loadQuiz2();
}

function initQuiz1() {
  const resultBtn = document.getElementById("resultBtn");
  if (!resultBtn) return;

  resultBtn.addEventListener("click", () => {
    const selected = document.querySelector('input[name="usage"]:checked');
    const resultDiv = document.getElementById("result");
    const optionsDiv = document.getElementById("options");

    if (!selected) {
      resultDiv.innerText = "하나를 선택해주세요 🌱";
      return;
    }

    const score = parseInt(selected.value);
    let message = "";

    if (score <= 2) {
      message = "💡 스마트폰 사용이 건강한 편이에요. 잘 하고 있어요!";
    } else if (score <= 4) {
      message = "🌥️ 약간의 주의가 필요해요. 조금씩 줄여봐요.";
    } else {
      message = "⚠️ 과의존 위험! 잠들기 1시간 전에는 스마트폰을 멀리해요.";
    }

    optionsDiv.style.display = "none";
    resultBtn.style.display = "none";
    resultDiv.innerText = `✨ 당신의 점수는 ${score}/5점입니다.\n${message}`;
  });
}

function initQuiz2() {
  const quizContainer = document.getElementById("quizContainer");
  const result = document.getElementById("result");

  if (!quizContainer || !result) return;

  const questions = [
    {
      question: "1. 스마트폰 중독은 WHO(세계보건기구)에서 공식 질병으로 분류되어 있다.",
      options: ["⭕ 그렇다", "❌ 아니다"],
      answer: "❌ 아니다",
      explanation: "현재 스마트폰 중독은 WHO의 공식 질병 분류에는 포함되어 있지 않습니다."
    },
    {
      question: "2. 눈을 깜빡이는 횟수는 스마트폰을 사용할수록 증가한다.",
      options: ["⭕ 그렇다", "❌ 아니다"],
      answer: "❌ 아니다",
      explanation: "스마트폰 사용 시 눈 깜빡임은 감소하여 안구건조증을 유발할 수 있습니다."
    },
    {
      question: "3. 어두운 곳에서 스마트폰을 보면 눈에 더 좋다.",
      options: ["⭕ 그렇다", "❌ 아니다"],
      answer: "❌ 아니다",
      explanation: "어두운 곳에서 화면을 보면 눈에 더 많은 피로와 손상을 줄 수 있습니다."
    },
    {
      question: "4. 스마트폰 블루라이트는 장기간 노출 시 망막 손상 가능성이 있다.",
      options: ["⭕ 그렇다", "❌ 아니다"],
      answer: "⭕ 그렇다",
      explanation: "블루라이트는 장기적으로 망막에 손상을 줄 수 있습니다."
    },
    {
      question: "5. 스마트폰의 알림 소리는 뇌에 도파민을 분비시켜 반복적인 확인 습관을 유도한다.",
      options: ["⭕ 그렇다", "❌ 아니다"],
      answer: "⭕ 그렇다",
      explanation: "알림은 뇌의 보상 시스템을 자극해 중독성을 유발할 수 있습니다."
    }
  ];

  let current = 0;
  let score = 0;

  function showQuestion(index) {
    const q = questions[index];
    quizContainer.innerHTML = `
      <div class="question-title">${q.question}</div>
      ${q.options.map(opt => `
        <label class="option">
          <input type="radio" name="q" value="${opt}"> ${opt}
        </label>
      `).join('')}
      <button id="submitAnswer">제출</button>
    `;
    result.innerHTML = "";
    document.getElementById("submitAnswer").onclick = checkAnswer;
  }

  function checkAnswer() {
    const selected = document.querySelector('input[name="q"]:checked');
    if (!selected) {
      result.innerText = "❗ 답을 선택해주세요!";
      return;
    }

    const answer = selected.value;
    const currentQ = questions[current];
    const allOptions = document.querySelectorAll('input[name="q"]');

    allOptions.forEach(input => {
      input.disabled = true;
      const label = input.parentElement;
      if (input.value === currentQ.answer) {
        label.style.fontWeight = "bold";
        label.style.backgroundColor = "#e2f4ea";
        label.style.color = "#2b7a0b";
        label.innerHTML = `✔️ ${label.innerHTML}`;
      } else if (input.checked && input.value !== currentQ.answer) {
        label.style.color = "#c0392b";
        label.innerHTML = `❌ ${label.innerHTML}`;
      }
    });

    if (answer === currentQ.answer) {
      score += 20;
      result.innerHTML = `✅ 정답입니다!<br><em>${currentQ.explanation}</em>`;
    } else {
      result.innerHTML = `❌ 오답입니다. 정답은 <strong style="color:#2b7a0b;">${currentQ.answer}</strong> 입니다.<br><em>${currentQ.explanation}</em>`;
    }

    document.getElementById("submitAnswer").style.display = "none";

    if (current < questions.length - 1) {
      quizContainer.innerHTML += `<button id="nextQuestion">다음 문제</button>`;
      document.getElementById("nextQuestion").onclick = () => {
        current++;
        showQuestion(current);
      };
    } else {
      result.innerHTML += `<br><br>🎯 퀴즈 종료!<br>총점: ${score}점`;
    }
  }

  showQuestion(current);
}
