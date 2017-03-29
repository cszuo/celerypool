
from celery import Celery
from celery import Task
import os
import imp
import time
import marshal


#workerNum = os.environ.get('workernum')
broker    = os.environ.get('rBroker')
backend   = os.environ.get('rBackend')
print "broker", broker
print "backend", backend
app = Celery('tasks', 
	broker  = broker,
	backend = backend,)

app.conf.update(
	CELERY_TRACK_STARTED=True,
	CELERYD_MAX_TASKS_PER_CHILD = 1,
)


@app.task()
def run(jtask):
	'''
	{
		'code':codeobject(base64encoded),
		'init':'init',
		'start':'start'.
		'args':args
	}
	'''
	try:
		mname = str(int(time.time()))
		modu = imp.new_module(mname)
		exec(marshal.loads(jtask['code'].decode('base64')),modu.__dict__)
	except Exception,e:
		return {'error':e}

	if 'init' in jtask:
		try:
			modu.__getattribute__(jtask['init'])()
		except Exception,e:
			return {'error':e}
	try:
		res = modu.__getattribute__(jtask['start'])(jtask['args'])
	except Exception,e:
		return {'error':e}
	return {'res':res}



