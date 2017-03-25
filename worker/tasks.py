
from celery import Celery
from celery import Task
import os



#workerNum = os.environ.get('workernum')
broker    = os.environ.get('rBroker')
backend   = os.environ.get('rBackend')

app = Celery('tasks', 
	broker  = broker,
	backend = backend,)

app.conf.update(
	CELERY_TRACK_STARTED=True,
	CELERYD_MAX_TASKS_PER_CHILD = 1,
)


@app.task()
def run(task):
	return 1



