from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from fastapi import FastAPI
from job.job import async_scheduled_job
from log import logger

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application Startup: Starting Scheduler...")
    scheduler.start()    
    scheduler.add_job(async_scheduled_job, 'interval', seconds=3600)

    yield 

    logger.info("Application Shutdown: Stopping Scheduler...")
    scheduler.shutdown()
    logger.info("Application Shutdown Complete.")
