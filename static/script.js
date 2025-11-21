let cortisolChart;
let chartData = {
    labels: [],
    values: []
};

const MAX_DATA_POINTS = 60;

function getStatusInfo(cortisol) {
    if (cortisol < 5) {
        return { text: 'Low Cortisol', class: 'low' };
    } else if (cortisol >= 5 && cortisol <= 18) {
        return { text: 'Normal', class: 'normal' };
    } else {
        return { text: 'High Cortisol', class: 'high' };
    }
}

function initChart() {
    const ctx = document.getElementById('cortisolChart').getContext('2d');
    
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(0, 217, 255, 0.4)');
    gradient.addColorStop(1, 'rgba(0, 217, 255, 0.0)');
    
    cortisolChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Cortisol Level (ng/mL)',
                data: chartData.values,
                borderColor: '#00D9FF',
                backgroundColor: gradient,
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#00D9FF',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            return 'Cortisol: ' + context.parsed.y.toFixed(2) + ' ng/mL';
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        color: '#6B7280',
                        maxRotation: 0
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        color: '#6B7280',
                        callback: function(value) {
                            return value.toFixed(0);
                        }
                    }
                }
            },
            animation: {
                duration: 750,
                easing: 'easeInOutQuart'
            }
        }
    });
}

async function fetchCortisolData() {
    try {
        const response = await fetch('/api/cortisol');
        const data = await response.json();
        
        updateDisplay(data);
        updateChart(data);
        
    } catch (error) {
        console.error('Error fetching cortisol data:', error);
    }
}

function updateDisplay(data) {
    const valueElement = document.getElementById('cortisolValue');
    const timestampElement = document.getElementById('timestamp');
    const statusBadge = document.getElementById('statusBadge');
    
    valueElement.style.opacity = '0';
    
    setTimeout(() => {
        valueElement.textContent = data.cortisol.toFixed(2);
        valueElement.style.opacity = '1';
    }, 150);
    
    timestampElement.textContent = `Updated: ${data.timestamp}`;
    
    const status = getStatusInfo(data.cortisol);
    statusBadge.textContent = status.text;
    statusBadge.className = 'status-badge ' + status.class;
}

function updateChart(data) {
    const timeLabel = new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    });
    
    chartData.labels.push(timeLabel);
    chartData.values.push(data.cortisol);
    
    if (chartData.labels.length > MAX_DATA_POINTS) {
        chartData.labels.shift();
        chartData.values.shift();
    }
    
    cortisolChart.update('none');
}

document.addEventListener('DOMContentLoaded', () => {
    initChart();
    fetchCortisolData();
    setInterval(fetchCortisolData, 1000);
});
