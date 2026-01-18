import psutil
import logging
from metrics import (
    machine_cpu_count,
    machine_cpu_utilisation,
    machine_memory_total,
    machine_memory_utilisation,
    machine_disk_read_bytes,
    machine_disk_write_bytes,
    machine_network_bytes_sent,
    machine_network_bytes_recv,
    disk_total_bytes,
    disk_utilisation_percentage,
)

logging.basicConfig(
  level=logging.INFO,
  format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetricsCollector:
  """Collects system metrics and updates Prometheus Gauges."""

  def __init__(self):
    """Initializes the MetricsCollector."""
    logger.info("Initialised MetricsCollector")

  def collect_cpu_metrics(self):
    """Collects CPU metrics."""
    try:
      cpu_count = psutil.cpu_count()
      if cpu_count is not None:
        machine_cpu_count.set(cpu_count)

        cpu_percent = psutil.cpu_percent(interval=None)
        machine_cpu_utilisation.set(cpu_percent)
        logger.debug(f"Collected CPU metrics: count={cpu_count}, utilisation={cpu_percent}%")
    except Exception as e:
      logger.error(f"Error collecting CPU metrics: {e}")

  def collect_memory_metrics(self):
    """Collects memory metrics."""
    try:
      virtual_memory = psutil.virtual_memory()
      total_memory = virtual_memory.total
      used_memory_percent = virtual_memory.percent
      logger.debug(f"Collected Memory metrics: total={total_memory} bytes, utilisation={used_memory_percent}%")
    except Exception as e:
        logger.error(f"Error collecting memory metrics: {e}")
  
  def collect_disk_io_metrics(self):
    """Collects disk I/O metrics."""
    try:

      disk_io = psutil.disk_io_counters()
      if disk_io is None:
        logger.warning("Disk I/O counters not available.")
        return;
      

    except Exception as e:
      logger.error(f"Error collecting Disk I/O metrics: {e}")