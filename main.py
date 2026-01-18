import asyncio
import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from prometheus_client import make_asgi_app

from collectors import MetricsCollector
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
  task = asyncio.create_task(collect_metrics_periodically())
  logger.info("Application started")
  yield

  task.cancel()
  try:
    await task
  except asyncio.CancelledError:
    pass
  logger.info("Application shutdown completed")

app = FastAPI(
  title="Machine Exporter",
  version="1.0.0",
  description="A Prometheus exporter for machine metrics using FastAPI and psutil.",
  lifespan=lifespan
  )

async def collect_metrics_periodically():
  collector = MetricsCollector()
  logger.info("Starting periodic metrics collection")

  try:
    while True:
      try:
        collector.collect_all_metrics()
        await asyncio.sleep(5)  
      except Exception as e:
        logger.error(f"Error in collecting metrics: {e}")
  except asyncio.CancelledError:
    logger.info("Metrics collection task cancelled")
    raise

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

def get_gauge_value(gauge):
  try:
    return gauge._value.get()
  except:
    return 0
  
@app.get("/api/metrics")
async def get_metrics_json():
  try:
    disks = []
    from metrics import disk_total_bytes, disk_utilisation_percentage
    import psutil
    partitions = psutil.disk_partitions()
    for partition in partitions:
      mountpoint = partition.mountpoint
      try:
        disks.append({
          "mountpoint": mountpoint,
          "total_bytes": get_gauge_value(disk_total_bytes.labels(mountpoint=mountpoint)),
          "utilisation": get_gauge_value(disk_utilisation_percentage.labels(mountpoint=mountpoint))
        })
      except: continue

      return {
        "cpu": {
          "count": get_gauge_value(cpu_count),
          "utilisation": get_gauge_value(cpu_utilisation)
        },
        "memory": {
          "total_bytes": get_gauge_value(memory_total),
          "utilisation": get_gauge_value(memory_utilisation)
        },
        "disk_io": {
          "read_bytes": get_gauge_value(disk_read_bytes),
          "write_bytes": get_gauge_value(disk_write_bytes)
        },
        "network": {
          "bytes_sent": get_gauge_value(network_bytes_sent),
          "bytes_recv": get_gauge_value(network_bytes_recv)
        },
        "disks": disks,
        "timestamp": asyncio.get_event_loop().time()
      }
  except Exception as e:
    logger.error(f"Error generating JSON metrics: {e}")
    return {"error": str(e)}