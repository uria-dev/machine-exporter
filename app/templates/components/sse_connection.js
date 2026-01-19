let previousNetworkData = null;
let previousDiskData = null;
let previousTimestamp = null;

function updateCharts(data) {
  const currentTimestamp = data.timestamp || Date.now() / 1000;

  const cpuUtil = data.cpu.utilisation || 0;
  cpuChart.data.datasets[0].data = [cpuUtil, 100 - cpuUtil];
  cpuChart.data.datasets[0].backgroundColor = [
    cpuUtil > 90 ? "#ef4444" : cpuUtil > 70 ? "#f59e0b" : "#10b981",
    "#e5e7eb",
  ];
  cpuChart.update();

  const memUtil = data.memory.utilisation || 0;
  memoryChart.data.datasets[0].data = [memUtil, 100 - memUtil];
  memoryChart.data.datasets[0].backgroundColor = [
    memUtil > 90 ? "#ef4444" : memUtil > 70 ? "#f59e0b" : "#10b981",
    "#e5e7eb",
  ];
  memoryChart.update();

  if (previousNetworkData && previousTimestamp) {
    const timeDiff = currentTimestamp - previousTimestamp;

    if (timeDiff > 0) {
      const sentRate =
        (data.network.bytes_sent - previousNetworkData.bytes_sent) / timeDiff;
      const recvRate =
        (data.network.bytes_recv - previousNetworkData.bytes_recv) / timeDiff;
      const readRate =
        (data.disk_io.read_bytes - previousDiskData.read_bytes) / timeDiff;
      const writeRate =
        (data.disk_io.write_bytes - previousDiskData.write_bytes) / timeDiff;

      const now = new Date().toLocaleTimeString();
      networkChart.data.labels.push(now);
      networkChart.data.datasets[0].data.push(Math.max(0, sentRate));
      networkChart.data.datasets[1].data.push(Math.max(0, recvRate));

      if (networkChart.data.labels.length > 60) {
        networkChart.data.labels.shift();
        networkChart.data.datasets[0].data.shift();
        networkChart.data.datasets[1].data.shift();
      }
      networkChart.update();

      // Update disk I/O chart
      diskIoChart.data.labels.push(now);
      diskIoChart.data.datasets[0].data.push(Math.max(0, readRate));
      diskIoChart.data.datasets[1].data.push(Math.max(0, writeRate));

      if (diskIoChart.data.labels.length > 60) {
        diskIoChart.data.labels.shift();
        diskIoChart.data.datasets[0].data.shift();
        diskIoChart.data.datasets[1].data.shift();
      }
      diskIoChart.update();
    }
  }

  previousNetworkData = data.network;
  previousDiskData = data.disk_io;
  previousTimestamp = currentTimestamp;

  if (data.disks && data.disks.length > 0) {
    diskUsageChart.data.labels = data.disks.map((d) => d.mountpoint);
    diskUsageChart.data.datasets[0].data = data.disks.map(
      (d) => d.utilisation,
    );
    diskUsageChart.update();
  }

  document.getElementById("lastUpdate").textContent =
    new Date().toLocaleTimeString();
}

function updateStatus(connected) {
  const dot = document.getElementById("statusDot");
  const text = document.getElementById("statusText");

  if (connected) {
    dot.classList.remove("disconnected");
    text.textContent = "Connected";
  } else {
    dot.classList.add("disconnected");
    text.textContent = "Disconnected - Reconnecting...";
  }
}

const eventSource = new EventSource("/api/stream");

eventSource.onmessage = function (event) {
  const data = JSON.parse(event.data);
  updateCharts(data);
  updateStatus(true);
};

eventSource.onerror = function (error) {
  console.error("SSE error:", error);
  updateStatus(false);
};

eventSource.onopen = function () {
  updateStatus(true);
};
