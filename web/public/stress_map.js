window.addEventListener("DOMContentLoaded", () => {
  kakao.maps.load(() => {
    drawStressMap(2024);
    drawBreakfastMap(2024);
  });
});

function updateMapByYear() {
  const year = parseInt(document.getElementById("map_year").value);
  if (!year || year < 2015 || year > 2024) {
    alert("2015~2024 사이의 연도를 입력해 주세요.");
    return;
  }
  drawStressMap(year);
}

function updateBreakfastMapByYear() {
  const year = parseInt(document.getElementById("breakfast_map_year").value);
  if (!year || year < 2015 || year > 2024) {
    alert("2015~2024 사이의 연도를 입력해 주세요.");
    return;
  }
  drawBreakfastMap(year);
}

// 지역 좌표 공통
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

function drawStressMap(year) {
  const map = new kakao.maps.Map(document.getElementById("map"), {
    center: new kakao.maps.LatLng(36.5, 128),
    level: 14
  });

  setTimeout(() => window.dispatchEvent(new Event('resize')), 300);

  const promises = Object.entries(regionCoords).map(async ([region, [lng, lat]]) => {
    const res = await fetch(`http://192.168.1.23:3001/stress_region?region=${region}&year=${year}`);
    const data = await res.json();
    return { region, lat, lng, rate: data?.stress_rate ?? null };
  });

  Promise.all(promises).then(results => {
    const validData = results.filter(r => r.rate !== null);
    const top3 = [...validData].sort((a, b) => b.rate - a.rate).slice(0, 3);

    top3.forEach(d => addCustomMarker(d, "#EF4444", map, 100)); // 빨강
    validData
      .filter(d => !top3.includes(d))
      .forEach(d => addCustomMarker(d, "#22C55E", map, 1)); // 초록
  });
}

function drawBreakfastMap(year) {
  const map = new kakao.maps.Map(document.getElementById("breakfast_map"), {
    center: new kakao.maps.LatLng(36.5, 128),
    level: 14
  });

  setTimeout(() => window.dispatchEvent(new Event('resize')), 300);

  const promises = Object.entries(regionCoords).map(async ([region, [lng, lat]]) => {
    const res = await fetch(`http://192.168.1.23:3001/breakfast_region?region=${region}&year=${year}`);
    const data = await res.json();
    return { region, lat, lng, rate: data?.breakfast_rate ?? null };
  });

  Promise.all(promises).then(results => {
    const validData = results.filter(r => r.rate !== null);
    const top3 = [...validData].sort((a, b) => b.rate - a.rate).slice(0, 3);

    top3.forEach(d => addCustomMarker(d, "#EF4444", map, 100)); // 빨강
    validData
      .filter(d => !top3.includes(d))
      .forEach(d => addCustomMarker(d, "#22C55E", map, 1)); // 초록
  });
}

function addCustomMarker({ region, lat, lng, rate }, color, map, zIndex = 1) {
  const content = `
    <div style="
      transform: scale(0.8); /* 전체 크기 80% */
      display: inline-block;
    ">
      <div style="
        background: ${color};
        padding: 6px 10px;
        border: 2px solid white;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        font-size: 12px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        line-height: 1.4;
      ">
        <div>${region}</div>
        <div>${rate}%</div>
      </div>
    </div>
  `;

  const marker = new kakao.maps.CustomOverlay({
    position: new kakao.maps.LatLng(lat, lng),
    content,
    yAnchor: 1,
    zIndex
  });

  marker.setMap(map);
}

