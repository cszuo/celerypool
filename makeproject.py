import os

cf = '''
{
	"rBroker" 	:	"",
	"rBackend"	:	""
}
'''.strip()

tsk = '''
import urllib2


def init():
	print 'init'

def start(arg):
	return urllib2.urlopen(arg).read().encode('base64')
'''.strip()

main = '''
import os,sys
sys.path.append('%s')

import celerypool

celerypool.initConfig()

celerypool.setFunction(os.path.split(os.path.realpath(__file__))[0] + '/task.py','init','start')

a = celerypool.start('http://google.com')

print a.get()['res'].decode('base64')
'''.strip()

def make(pname):
	if os.path.exists(pname):
		print 'Dir %s is exists!' % pname
		return
	os.mkdir(pname)
	if not os.path.exists(pname):
		print 'Make dir %s failed!' % pname
		return

	f = open('%s/config.json' % pname,'w')
	f.write(cf)
	f.close()

	f = open('%s/task.py' % pname,'w')
	f.write(tsk)
	f.close()

	f = open('%s/main.py' % pname,'w')
	f.write(main%os.path.split(os.path.realpath(__file__))[0])
	f.close()

	print 'Project %s done!' % pname