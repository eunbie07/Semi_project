
window.addEventListener('DOMContentLoaded', () => {
  const content = document.querySelector('.content');
  content.classList.add('home-fullscreen'); // 첫 로딩 시 홈 탭이라면 여백 제거
});

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


async function getDepression() {
  const age = parseInt(document.getElementById("age").value);
  const gender = document.getElementById("gender").value;
  const year = parseInt(document.getElementById("year").value);
  const resultEl = document.getElementById("result");

  const genderKor = gender === "male" ? "남학생" : "여학생";

  if (isNaN(age) || isNaN(year)) {
    resultEl.innerHTML = `<span class="warning">나이와 연도를 입력해 주세요.</span>`;
    return;
  }

  try {
    resultEl.innerHTML = "<span class='loading'>데이터를 불러오는 중...</span>";
    const res = await fetch(`/api/depression?age=${age}&gender=${gender}&year=${year}`);
    const data = await res.json();

    console.log("[응답 확인]", data);

    if (data.depression_rate == null || isNaN(data.depression_rate)) {
      resultEl.innerHTML = `<span class='notfound'> 해당 정보가 없습니다.</span>`;
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
    resultEl.innerHTML = `<span class='error'>서버 오류 또는 연결 실패.</span>`;
  }
}