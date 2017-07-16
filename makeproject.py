import os

cf = '''
{
	"rBroker" 	:	"",
	"rBackend"	:	""
}
'''.strip()

tsk = '''
import urllib2
import ssl, json, OpenSSL.crypto, time, gevent
from gevent import Timeout
from gevent.pool import Pool
import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()


def init():
	print 'init'

rests = []

def handle_cert(ip,cert):
	info = {}
	for i in cert.get_subject().get_components():
		if i[0] in ('CN'):
			info[i[0]] = i[1]
	res = json.dumps(info['CN']).replace('"','')
	print res
	rests.append('%s:%s'%(ip,res))

def getcer(ip):
	global res
	for i in (2,3):
		try:
			cert = ssl.get_server_certificate((ip, 443), ssl_version=i) 
			cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
			handle_cert(ip,cert);#return cert;
		except Exception, e:
			if 'wrong version number' in str(e):
				continue
			else:
				print ip, e
def worker(ip):
	try:
		with Timeout(8):
			getcer(ip)
	except:
		pass

def start(arg):
	pool = Pool(100)
	for i in arg:
		pool.spawn(worker, i)
	pool.join()
	return rests
'''.strip()

main = '''
import os,sys,time
sys.path.append('/private/tmp/celerypool')

import celerypool
celerypool.initConfig()
celerypool.setFunction(os.path.split(os.path.realpath(__file__))[0] + '/task.py','init','start')

rests = []
maxl = 200
dt = time.strftime("%Y-%m-%d")

def callback(res):
	print len(res)
	with open('certs_%s.txt' % dt,'a+') as f:
		for i in res:
			f.write(i + '\n')

idel = maxl
for i in range(10):
	if idel <= 0:
		idel = celerypool.wait_for_next_idel(callback, maxl)
	else:
		idel -= 1
	celerypool.start(['google.com']*100)
	print i

while celerypool.wait_for_next_idel(callback, maxl) != maxl:
	time.sleep(5)'''.strip()

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