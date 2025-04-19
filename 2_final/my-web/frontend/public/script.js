// 부드러운 전환 애니메이션과 스타일 요소를 고려한 UI용 JS

function showTab(tabId) {
  const tabs = document.querySelectorAll(".tab");
  tabs.forEach(tab => {
    tab.classList.remove("active");
    tab.style.opacity = 0;
  });

  const targetTab = document.getElementById(tabId);
  targetTab.classList.add("active");
  setTimeout(() => targetTab.style.opacity = 1, 50);
}


async function getDepression() {
  const age = parseInt(document.getElementById("age").value);
  const gender = document.getElementById("gender").value;
  const year = parseInt(document.getElementById("year").value);
  const resultEl = document.getElementById("result");

  const genderKor = gender === "male" ? "남학생" : "여학생";

  if (isNaN(age) || isNaN(year)) {
    resultEl.innerHTML = `<span class="warning">⚠️ 나이와 연도를 입력해 주세요.</span>`;
    return;
  }

  try {
    resultEl.innerHTML = "<span class='loading'>데이터를 불러오는 중...</span>";
    const res = await fetch(`http://localhost:8000/depression?age=${age}&gender=${gender}&year=${year}`);
    const data = await res.json();

    console.log("[응답 확인]", data);

    if (data.depression_rate == null || isNaN(data.depression_rate)) {
      resultEl.innerHTML = `<span class='notfound'>😥 해당 정보가 없습니다.</span>`;
    } else {
      resultEl.innerHTML = `
        <div class="result-box">
          <h3>${year}년 ${age}세 ${genderKor}의 우울감 경험률은</h3>
          <div class="rate">${data.depression_rate}%</div>
        </div>
      `;
    }
  } catch (err) {
    console.error(err);
    resultEl.innerHTML = `<span class='error'>🚨 서버 오류 또는 연결 실패.</span>`;
  }
}