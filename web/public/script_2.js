

const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');

menuToggle.addEventListener('click', () => {
  sidebar.classList.toggle('active');
});


window.addEventListener("DOMContentLoaded", () => {
  const content = document.querySelector('.content');
  content.classList.add('home-fullscreen');

  kakao.maps.load(() => {
    window.kakaoMapsLoaded = true;
    drawStressMap(2022); // 기본 연도a
  });
});



function showTab(tabId) {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => {
    tab.style.display = tab.id === tabId ? "block" : "none";
    tab.classList.toggle("active", tab.id === tabId);
  });

  const content = document.querySelector('.content');
  content.classList.toggle('home-fullscreen', tabId === 'home');

  if (tabId === 'stress_region') {
    const tryDraw = () => {
      if (window.kakao && window.kakao.maps && window.kakaoMapsLoaded) {
        const year = parseInt(document.getElementById("map_year").value) || 2022;
        drawStressMap(year);
      } else {
        setTimeout(tryDraw, 100);
      }
    };
    tryDraw();
  }

  
  if (tabId === 'breakfast_region') {
    const tryDraw = () => {
      if (window.kakao && window.kakao.maps && window.kakaoMapsLoaded) {
        const year = parseInt(document.getElementById("breakfast_map_year").value) || 2024;
        drawBreakfastMap(year);
      } else {
        setTimeout(tryDraw, 100);
      }
    };
    tryDraw();
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
    const res = await fetch(`/api/stress_top_issue?year=${year}`);
    const data = await res.json();

    if (!data.result || !data["top_issue"]) {
      resultEl.innerHTML = `<span class='notfound'>해당 데이터가 없습니다.</span>`;
    } else {
      const translatedIssue = issueTranslate[data["top_issue"]] || data["top_issue"];
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
    const res = await fetch(`/api/smartphone_badeffect?age=${age}&year=${year}`);
    const data = await res.json();

    if (!data.resultCode) {
      resultEl.innerHTML = `<span class='notfound'> 해당 정보가 없습니다.</span>`;
    } else {
      resultEl.innerHTML = `
        <div class="result-box">
          <h3>${data.year}년 ${data.group}의 스마트폰 부정적 영향</h3>
          <ul>
            <li>스마트폰 이용시간 줄이기 실패율: <strong>${data.fail_to_reduce_rate}%</strong></li>
            <li>가족과 갈등 경험률: <strong>${data.family_conflict_rate}%</strong></li>
            <li>친구와 갈등 경험률: <strong>${data.social_conflict_rate}%</strong></li>
          </ul>
        </div>
      `;
    }
  } catch (err) {
    console.error(err);
    resultEl.innerHTML = `<span class='error'>스마트폰 데이터 로드 실패.</span>`;
  }
}


function updateMapByYear() {
  const year = parseInt(document.getElementById("map_year").value);
  if (isNaN(year) || year < 2015 || year > 2024) {
    alert("2015년부터 2024년까지의 연도만 입력 가능합니다.");
    return;
  }
  drawStressMap(year);
}

function drawStressMap(year = 2024) {
  const regionCoords = {
    "서울": [126.9780, 37.5665], "부산": [129.0756, 35.1796],
    "대구": [128.6014, 35.8714], "인천": [126.7052, 37.4563],
    "광주": [126.8514, 35.1600], "대전": [127.3845, 36.3504],
    "울산": [129.3114, 35.5384], "세종": [127.2891, 36.4800],
    "경기": [127.5183, 37.4138], "강원": [128.3115, 37.8228],
    "충북": [127.4914, 36.6358], "충남": [126.8635, 36.5184],
    "전북": [127.1088, 35.8218], "전남": [126.4629, 34.8161],
    "경북": [128.8889, 36.4919], "경남": [128.2132, 35.4606],
    "제주": [126.5312, 33.4996]
  };

  const map = new kakao.maps.Map(document.getElementById('map'), {
    center: new kakao.maps.LatLng(36.5, 128.3),
    level: 14
  });

  const promises = Object.entries(regionCoords).map(async ([region, [lng, lat]]) => {
    const res = await fetch(`http://192.168.1.23:3001/stress_region?region=${region.trim()}&year=${year}`);
    const data = await res.json();
    return { region, lat, lng, stress_rate: data?.stress_rate ?? null };
  });

  Promise.all(promises).then(results => {
    const validData = results.filter(r => r.stress_rate !== null);
    const top3Regions = validData
      .sort((a, b) => b.stress_rate - a.stress_rate)
      .slice(0, 3)
      .map(r => r.region);

    
    top3Regions.forEach(topRegion => {
      const topData = validData.find(d => d.region === topRegion);
      if (topData) addMarker(topData, "#EF4444", map, 100);
    });

    
    validData
      .filter(d => !top3Regions.includes(d.region))
      .forEach(data => addMarker(data, "#22C55E", map, 1));
  });
}


function addMarker({ region, lat, lng, stress_rate }, color, map, zIndex = 1) {
  const markerHtml = `
    <div class="marker-label" style="background:${color}; text-align:center;">
      <div style="font-size:12px; font-weight:bold;">${region}</div>
      <div>${stress_rate}%</div>
    </div>
  `;

  const marker = new kakao.maps.CustomOverlay({
    position: new kakao.maps.LatLng(lat, lng),
    content: markerHtml,
    yAnchor: 1,
    zIndex: zIndex
  });

  marker.setMap(map);
}

const chartSelect = document.getElementById("chart_year");
let chartRoot;

function drawStressDonut(data, year) {
  if (chartRoot) chartRoot.dispose();

  am5.ready(() => {
    chartRoot = am5.Root.new("chartdiv");

    chartRoot.setThemes([am5themes_Animated.new(chartRoot)]);

    const chart = chartRoot.container.children.push(
      am5percent.PieChart.new(chartRoot, {
        layout: chartRoot.verticalLayout
      })
    );

    const series = chart.series.push(
      am5percent.PieSeries.new(chartRoot, {
        valueField: "concern_rate",
        categoryField: "issue",
        innerRadius: am5.percent(50)
      })
    );

    series.data.setAll(data);

    chart.children.push(
      am5.Label.new(chartRoot, {
        text: `${year}년`,
        fontSize: 24,
        centerX: am5.percent(50),
        centerY: am5.percent(50),
        fill: am5.color(0x444444)
      })
    );
  });
}

function loadStressDonut(year) {
  fetch(`http://192.168.1.23:3001/stress_issues?year=${year}`)
    .then(res => res.json())
    .then(data => drawStressDonut(data, year));
}

// 초기 로딩
chartSelect.addEventListener("change", () => {
  loadStressDonut(chartSelect.value);
});

// 탭이 stress_chart일 때 차트 로딩
if (typeof showTab === "function") {
  const originalShowTab = showTab;
  showTab = function (tabId) {
    originalShowTab(tabId);
    if (tabId === "stress_chart") {
      loadStressDonut(chartSelect.value);
    }
  };
}



function updateBreakfastMapByYear() {
  const year = parseInt(document.getElementById("breakfast_map_year").value);
  if (isNaN(year) || year < 2015 || year > 2024) {
    alert("2015년부터 2024년까지의 연도만 입력 가능합니다.");
    return;
  }
  drawBreakfastMap(year);
}

function drawBreakfastMap(year = 2024) {
  const regionCoords = {
    "서울": [126.9780, 37.5665], "부산": [129.0756, 35.1796],
    "대구": [128.6014, 35.8714], "인천": [126.7052, 37.4563],
    "광주": [126.8514, 35.1600], "대전": [127.3845, 36.3504],
    "울산": [129.3114, 35.5384], "세종": [127.2891, 36.4800],
    "경기": [127.5183, 37.4138], "강원": [128.3115, 37.8228],
    "충북": [127.4914, 36.6358], "충남": [126.8635, 36.5184],
    "전북": [127.1088, 35.8218], "전남": [126.4629, 34.8161],
    "경북": [128.8889, 36.4919], "경남": [128.2132, 35.4606],
    "제주": [126.5312, 33.4996]
  };

  const map = new kakao.maps.Map(document.getElementById('breakfast_map'), {
    center: new kakao.maps.LatLng(36.5, 128.3),
    level: 14
  });

  const promises = Object.entries(regionCoords).map(async ([region, [lng, lat]]) => {
    const res = await fetch(`http://192.168.1.23:3001/breakfast_region?region=${region}&year=${year}`);
    const data = await res.json();
    return { region, lat, lng, breakfast_rate: data?.breakfast_rate ?? null };
  });

  Promise.all(promises).then(results => {
    const validData = results.filter(r => r.breakfast_rate !== null);
    const top3Regions = validData
      .sort((a, b) => b.breakfast_rate - a.breakfast_rate)
      .slice(0, 3)
      .map(r => r.region);

    
    top3Regions.forEach(topRegion => {
      const topData = validData.find(d => d.region === topRegion);
      if (topData) addBreakfastMarker(topData, "#EF4444", map, 100);
    });

    
    validData
      .filter(d => !top3Regions.includes(d.region))
      .forEach(data => addBreakfastMarker(data, "#22C55E", map, 1));
  });
}

function addBreakfastMarker({ region, lat, lng, breakfast_rate }, color, map, zIndex = 1) {
  const markerHtml = `
    <div class="marker-label" style="background:${color}; text-align:center;">
      <div style="font-size:12px; font-weight:bold;">${region}</div>
      <div>${breakfast_rate}%</div>
    </div>
  `;

  const marker = new kakao.maps.CustomOverlay({
    position: new kakao.maps.LatLng(lat, lng),
    content: markerHtml,
    yAnchor: 1,
    zIndex: zIndex
  });

  marker.setMap(map);
}

if (tabId === 'breakfast_region') {
  const tryDraw = () => {
    if (window.kakao && window.kakao.maps && window.kakaoMapsLoaded) {
      const year = parseInt(document.getElementById("breakfast_map_year").value) || 2024;
      drawBreakfastMap(year);
    } else {
      setTimeout(tryDraw, 100);
    }
  };
  tryDraw();
}