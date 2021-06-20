#Run: celery -A tasks worker --loglevel=INFO --pool=solo
#precondicion: docker run --name some-redis -p 6379:6379 -d redis

from celery import Celery

REDIS = 'redis://localhost:6379'
celery = Celery(__name__, backend=REDIS, broker=REDIS)

@celery.task(name='heavy')
def double(x):
    return 2*x