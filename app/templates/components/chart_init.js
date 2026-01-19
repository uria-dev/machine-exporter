const gaugeOptions = {
  type: "doughnut",
  options: {
    circumference: 180,
    rotation: 270,
    cutout: "75%",
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
    animation: { animateRotate: true, duration: 500 },
  },
};
const cpuChart = new Chart(document.getElementById("cpuChart"), {
  ...gaugeOptions,
  data: {
    datasets: [
      {
        data: [0, 100],
        backgroundColor: ["#667eea", "#e5e7eb"],
        borderWidth: 0,
      },
    ],
  },
});
const memoryChart = new Chart(document.getElementById("memoryChart"), {
  ...gaugeOptions,
  data: {
    datasets: [
      {
        data: [0, 100],
        backgroundColor: ["#f59e0b", "#e5e7eb"],
        borderWidth: 0,
      },
    ],
  },
});
const networkChart = new Chart(document.getElementById("networkChart"), {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Bytes Sent/sec",
        data: [],
        borderColor: "#10b981",
        backgroundColor: "rgba(16, 185, 129, 0.1)",
        tension: 0.4,
      },
      {
        label: "Bytes Received/sec",
        data: [],
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        tension: 0.4,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { beginAtZero: true } },
    plugins: { legend: { position: "top" } },
  },
});
const diskIoChart = new Chart(document.getElementById("diskIoChart"), {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Read Bytes/sec",
        data: [],
        borderColor: "#8b5cf6",
        backgroundColor: "rgba(139, 92, 246, 0.1)",
        tension: 0.4,
      },
      {
        label: "Write Bytes/sec",
        data: [],
        borderColor: "#ec4899",
        backgroundColor: "rgba(236, 72, 153, 0.1)",
        tension: 0.4,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { beginAtZero: true } },
    plugins: { legend: { position: "top" } },
  },
});
const diskUsageChart = new Chart(document.getElementById("diskUsageChart"), {
  type: "bar",
  data: {
    labels: [],
    datasets: [
      {
        label: "Disk Usage %",
        data: [],
        backgroundColor: "#667eea",
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: "y",
    scales: { x: { beginAtZero: true, max: 100 } },
  },
});
