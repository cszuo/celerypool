#!/usr/bin/python
import json
import sys
import os,time
import base64
import marshal


args = {}
runfunction = None

def initConfig():
	'''load Broker and Backend information and import task'''
	global runfunction
	conf = json.loads(open('config.json').read())
	os.environ.update(conf)
	sys.path.append(os.path.split(os.path.realpath(__file__))[0] + "/worker")
	from tasks import run
	runfunction = run


def setFunction(pyfile,init,start):
	'''args are all string'''
	code = open(pyfile).read()
	codeobj = compile(code, '<string>', 'exec')
	args['code'] = base64.b64encode(marshal.dumps(codeobj))
	args['init'] = init
	args['start'] = start


def start(param):
	args['args'] = param
	return runfunction.delay(args)

finishedtasks = []
def wait_for_next_idel(callback, maxl):
	while 1:
		for i in runfunction.backend.client.keys():
			i = i.replace('celery-task-meta-','')
			ar = runfunction.AsyncResult(i)
			if ar.state == u'SUCCESS' and ar.id not in finishedtasks:
				callback(ar.get()['res'])
				finishedtasks.append(ar.id)
			if ar.id in finishedtasks:
				ar.forget()
		rc = len(runfunction.backend.client.keys())
		if rc < maxl:
			return maxl - rc
		time.sleep(1)




if __name__ == '__main__':
	if len(sys.argv) == 3 and sys.argv[1] == 'newproject' and sys.argv[2] != None:
		import makeproject
		makeproject.make(sys.argv[2])
	else:
		print 'usage: THIS newproject projectname'