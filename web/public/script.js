
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

async function getStressIssues() {
  const year = parseInt(document.getElementById("si_year").value);
  const resultEl = document.getElementById("resultStress");

  if (isNaN(year)) {
    resultEl.innerHTML = `<span class="warning">연도를 입력해 주세요.</span>`;
    return;
  }

  // 영어 이슈 → 한국어 매핑
  const issueTranslate = {
    "Appearance": "외모",
    "Physical and Mental Health": "신체 및 정신 건강",
    "Family": "가정",
    "Finance": "경제 상황",
    "Allowance": "용돈",
    "Study": "학업",
    "Career": "진로",
    "Friends": "친구 관계",
    "Romantic Relationships": "이성 교제",
    "School Violence": "학교 폭력",
    "Smoking_Drinking_Substance Abuse": "흡연/음주/약물 남용",
    "SNS_Games": "SNS 및 게임",
    "Others": "기타",
    "No Concerns": "고민 없음"
  };

  try {
    resultEl.innerHTML = "<span class='loading'>데이터를 불러오는 중...</span>";

    const res = await fetch(`http://192.168.1.23:3001/stress_top_issue?year=${year}`);
    if (!res.ok) throw new Error("서버 응답 실패");

    const data = await res.json();
    console.log("[스트레스 이슈 응답]", data);

    if (!data.result || !data["top_issue"]) {
      resultEl.innerHTML = `<span class='notfound'>해당 데이터가 없습니다.</span>`;
    } else {
      const translatedIssue = issueTranslate[data["top_issue"]] || data["top_issue"]; // 매핑이 없으면 원래 값 사용

      resultEl.innerHTML = `
        <div class="result-box">
          <h3>${year}년 청소년의 가장 큰 스트레스 요인은</h3>
          <p><strong>${translatedIssue}</strong>입니다.</p>
          <p>비율: <strong>${data["concern_rate(%)"]}%</strong></p>
        </div>
      `;
    }
  } catch (err) {
    console.error(err);
    resultEl.innerHTML = `<span class='error'>서버 오류 또는 연결 실패.</span>`;
  }
}



async function getSmartphoneBadeffect() {
  const age = parseInt(document.getElementById("sp_age").value);
  const year = parseInt(document.getElementById("sp_year").value);
  const resultEl = document.getElementById("resultSmartphone");

  if (isNaN(age) || isNaN(year)) {
    resultEl.innerHTML = `<span class="warning">나이와 연도를 입력해 주세요.</span>`;
    return;
  }

  try {
    resultEl.innerHTML = "<span class='loading'>데이터를 불러오는 중...</span>";
    const res = await fetch(`http://192.168.1.53:3001/smartphone_badeffect?age=${age}&year=${year}`);
    const data = await res.json();

    console.log("[스마트폰 과의존 응답 확인]", data);

    if (!data.resultCode) {
      resultEl.innerHTML = `<span class='notfound'> 해당 정보가 없습니다.</span>`;
    } else {
      resultEl.innerHTML = `
        <div class="result-box">
          <h3>${data.year}년 ${data.group}의 스마트폰 부정적 영향</h3>
          <ul>
            <li>스마트폰 이용시간 줄이기 실패율: <strong>${data.fail_rate}%</strong></li>
            <li>가족과 갈등 경험률: <strong>${data.family_rate}%</strong></li>
            <li>친구와 갈등 경험률: <strong>${data.friends_rate}%</strong></li>
          </ul>
        </div>
      `;
    }
  } catch (err) {
    console.error(err);
    resultEl.innerHTML = `<span class='error'>스마트폰 데이터 로드 실패.</span>`;
  }
}