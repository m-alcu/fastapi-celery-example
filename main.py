#Run: uvicorn main:app --reload
#precondicion: docker run --name some-redis -p 6379:6379 -d redis

from fastapi import FastAPI, BackgroundTasks
from celery import Celery
import logging

app = FastAPI()

REDIS = 'redis://localhost:6379'
celery = Celery(__name__, backend=REDIS, broker=REDIS)

log = logging.getLogger(__name__)

def celery_on_message(body):
    log.warn(body)

def background_on_message(task):
    log.warn(task.get(on_message=celery_on_message, propagate=False))

@app.get("/{x}")
async def root( x: int,  background_task: BackgroundTasks):
    task = celery.send_task('heavy', args=[x])
    print(task)
    background_task.add_task(background_on_message, task)
    
    return {"message": "doubled"}