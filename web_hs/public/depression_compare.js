// ✅ CDN에서 ChartDataLabels 로드 필요
// index.html head에 추가: 
//<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0"></script>

// ✅ Chart.js 플러그인 등록
const API_BASE = "http://192.168.1.23:3001/depression";
let barChart, lineChart;
Chart.register(ChartDataLabels);

async function getDepressionRate(year, age, gender) {
  const url = `${API_BASE}?year=${year}&age=${age}&gender=${gender}`;
  const res = await fetch(url);
  const data = await res.json();
  return data.depression_rate;
}

async function updateCharts() {
  const year = parseInt(document.getElementById('yearSelect').value);
  const age = parseInt(document.getElementById('ageSelect').value);
  if (isNaN(year) || isNaN(age)) {
    alert("나이와 연도를 정확히 선택해주세요.");
    return;
  }

  document.getElementById('chartWrapper').style.display = 'flex';

  const [male, female, total, totalPrev] = await Promise.all([
    getDepressionRate(year, age, "male"),
    getDepressionRate(year, age, "female"),
    getDepressionRate(year, age, "전체"),
    getDepressionRate(year - 1, age, "전체").catch(() => null)
  ]);

  // ✅ Bar Chart
  const ctx1 = document.getElementById('depressionBarChart').getContext('2d');
  if (barChart) barChart.destroy();
  barChart = new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: [year],
      datasets: [
        {
          label: '남학생',
          data: [male],
          backgroundColor: '#8cc9f0',
          borderRadius: 12,
          barThickness: 40
        },
        {
          label: '여학생',
          data: [female],
          backgroundColor: '#d59ef2',
          borderRadius: 12,
          barThickness: 40
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        tooltip: { mode: 'index', intersect: false },
        datalabels: {
          color: '#333',
          anchor: 'end',
          align: 'top',
          font: { weight: 'bold' },
          formatter: (v) => v + '%'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 40,
          grid: { display: false },
          title: { display: true, text: '우울감 경험률 (%)' }
        },
        x: {
          grid: { display: false },
          title: { display: true, text: '연도' }
        }
      }
    },
    plugins: [ChartDataLabels]
  });

  // ✅ Line Chart
  const years = Array.from({ length: 10 }, (_, i) => 2015 + i);
  const maleSeries = await Promise.all(years.map(y => getDepressionRate(y, age, "male").catch(() => null)));
  const femaleSeries = await Promise.all(years.map(y => getDepressionRate(y, age, "female").catch(() => null)));

  const ctx2 = document.getElementById('depressionLineChart').getContext('2d');
  if (lineChart) lineChart.destroy();
  lineChart = new Chart(ctx2, {
    type: 'line',
    data: {
      labels: years,
      datasets: [
        {
          label: '남학생',
          data: maleSeries,
          borderColor: '#8cc9f0',
          backgroundColor: 'rgba(140, 201, 240, 0.25)',
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6
        },
        {
          label: '여학생',
          data: femaleSeries,
          borderColor: '#d59ef2',
          backgroundColor: 'rgba(213, 158, 242, 0.25)',
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        tooltip: { mode: 'index', intersect: false }
      },
      scales: {
        y: {
          beginAtZero: false,
          max: 40,
          grid: { display: false },
          title: { display: true, text: '우울감 경험률 (%)' }
        },
        x: {
          grid: { display: false },
          title: { display: true, text: '연도' }
        }
      }
    }
  });

  const commentBox = document.getElementById('changeComment');
  const diff = female - male;
  const genderComment = `📊 여학생이 남학생보다 ${year}년도 우울감 경험률이 ${Math.abs(diff).toFixed(1)}% ${diff > 0 ? "더 높습니다" : "더 낮습니다"}.`;
  const totalDiff = totalPrev != null ? total - totalPrev : null;
  const totalComment = totalDiff != null
    ? `📈 작년 대비 전체 우울감 경험률이 ${Math.abs(totalDiff).toFixed(1)}% ${totalDiff > 0 ? "⬆️ 증가" : "⬇️ 감소"}했습니다.`
    : "작년 데이터가 없어 변화율을 계산할 수 없습니다.";
  commentBox.innerText = `${genderComment}\n${totalComment}`;
}
