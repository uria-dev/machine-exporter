import psutil
import logging
from metrics import (
    cpu_count,
    cpu_utilisation,
    memory_total,
    memory_utilisation,
    disk_read_bytes,
    disk_write_bytes,
    network_bytes_sent,
    network_bytes_recv,
    disk_total_bytes,
    disk_utilisation_percentage,
)

logging.basicConfig(
  level=logging.INFO,
  format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetricsCollector:

  def __init__(self):
    logger.info("Initialised MetricsCollector")

  def collect_cpu_metrics(self):
    try:
      cpu_num = psutil.cpu_count()
      if cpu_num is not None:
        cpu_count.set(cpu_num)

        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_utilisation.set(cpu_percent)
        logger.debug(f"Collected CPU metrics: count={cpu_count}, utilisation={cpu_percent}%")
    except Exception as e:
      logger.error(f"Error collecting CPU metrics: {e}")

  def collect_memory_metrics(self):
    try:
      virtual_memory = psutil.virtual_memory()
      memory_total.set(virtual_memory.total)
      memory_utilisation.set(virtual_memory.percent)
      total_memory = virtual_memory.total
      used_memory_percent = virtual_memory.percent
      logger.debug(f"Collected Memory metrics: total={total_memory} bytes, utilisation={used_memory_percent}%")
    except Exception as e:
        logger.error(f"Error collecting memory metrics: {e}")
  
  def collect_disk_io_metrics(self):
    try:
      disk_io = psutil.disk_io_counters()
      if disk_io is None:
        logger.warning("Disk I/O counters not available.")
        return;
      disk_read_bytes.set(disk_io.read_bytes)
      disk_write_bytes.set(disk_io.write_bytes)
      logger.debug(f"Collected Disk I/O metrics: read_bytes={disk_io.read_bytes}, write_bytes={disk_io.write_bytes}")
    except Exception as e:
      logger.error(f"Error collecting Disk I/O metrics: {e}")
  def collect_disk_utilisation_metrics(self):
    try:
      partitions = psutil.disk_partitions()
      for partition in partitions:
        try:
          usage = psutil.disk_usage(partition.mountpoint)
          disk_total_bytes.labels(mountpoint=partition.mountpoint).set(usage.total)
          disk_utilisation_percentage.labels(mountpoint=partition.mountpoint).set(usage.percent)
          logger.debug(f"Collected Disk utilisation metrics for {partition.mountpoint}: total={usage.total} bytes, utilisation={usage.percent}%")
        except PermissionError:
          logger.warning(f"Permission denied accessing disk usage for partition {partition.mountpoint}")
    except Exception as e:
      logger.error(f"Error collecting Disk utilisation metrics: {e}")
  def collect_network_metrics(self):
    try:
      net_io = psutil.net_io_counters()
      if net_io is None:
        logger.warning("Network I/O counters not available.")
        return;
      network_bytes_sent.set(net_io.bytes_sent)
      network_bytes_recv.set(net_io.bytes_recv)
      logger.debug(f"Collected Network metrics: bytes_sent={net_io.bytes_sent}, bytes_recv={net_io.bytes_recv}")
    except Exception as e:
      logger.error(f"Error collecting Network metrics: {e}")
  
  def collect_all_metrics(self):
    try:
      logger.debug("Collecting metrics...")
      self.collect_cpu_metrics()
      self.collect_memory_metrics()
      self.collect_disk_io_metrics()
      self.collect_disk_utilisation_metrics()
      self.collect_network_metrics()
      logger.debug("All metrics collected.")
    except Exception as e:
      logger.error(f"Error collecting all metrics: {e}")
