// bio.js
document.addEventListener("DOMContentLoaded", () => {
    const today = new Date().toISOString().slice(0, 10);
    const startDateInput = document.getElementById("startdate");
    if (startDateInput) startDateInput.value = today;
  });
  
  function drawBiorhythm() {
    const birth = new Date(document.getElementById("birthdate").value);
    const start = new Date(document.getElementById("startdate").value);
  
    if (isNaN(birth) || isNaN(start)) {
      alert("생년월일과 시작일을 모두 선택해주세요!");
      return;
    }
  
    const labels = [];
    const physical = [];
    const emotional = [];
    const intellectual = [];
  
    for (let i = 0; i < 7; i++) {
      const current = new Date(start);
      current.setDate(start.getDate() + i);
      const days = Math.floor((current - birth) / (1000 * 60 * 60 * 24));
      labels.push(current.toISOString().slice(5, 10));
      physical.push(Math.sin((2 * Math.PI * days) / 23) * 100);
      emotional.push(Math.sin((2 * Math.PI * days) / 28) * 100);
      intellectual.push(Math.sin((2 * Math.PI * days) / 33) * 100);
    }
  
    const ctx = document.getElementById('biorhythmChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: '💪 신체',
            data: physical,
            borderColor: '#f48fb1',
            backgroundColor: 'rgba(244, 143, 177, 0.2)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointBackgroundColor: '#f48fb1',
          },
          {
            label: '💖 감정',
            data: emotional,
            borderColor: '#81d4fa',
            backgroundColor: 'rgba(129, 212, 250, 0.2)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointBackgroundColor: '#81d4fa',
          },
          {
            label: '🧠 지적',
            data: intellectual,
            borderColor: '#aed581',
            backgroundColor: 'rgba(174, 213, 129, 0.2)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointBackgroundColor: '#aed581',
          }
        ]
      },
      options: {
        responsive: false,
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        },
        scales: {
          y: {
            min: -100,
            max: 100,
            title: {
              display: true,
              text: '컨디션 (%)',
              color: '#666',
              font: {
                size: 14,
                weight: 'bold'
              }
            },
            grid: {
              color: '#eee'
            }
          },
          x: {
            ticks: {
              autoSkip: true,
              maxTicksLimit: 4,
              color: '#666'
            },
            grid: {
              color: '#f0f0f0'
            }
          }
        },
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#444',
              font: {
                size: 14
              }
            }
          },
          title: {
            display: false
          },
          tooltip: {
            backgroundColor: '#fff',
            titleColor: '#000',
            bodyColor: '#444',
            borderColor: '#ccc',
            borderWidth: 1
          }
        }
      }
    });
  }
  