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
