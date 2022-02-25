#!/usr/bin/python

import requests
import sys, os
import threading

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

threadLimiter = threading.BoundedSemaphore(10)

protos = ['http', 'https']

outputDir = "./robots.txt-files"
inputFile = "./web-domains.txt"

if not os.path.exists(outputDir):
	os.makedirs(outputDir)

def getRobots(proto, domain):
	threadLimiter.acquire()

	url = "%s://%s/robots.txt" % (proto, domain)

	try:
		sys.stdout.write("\033[K%s\r" % url)
		sys.stdout.flush()
		r = requests.get(url, verify=False, timeout=1)
		if r.status_code == 200:
			print("=== %s ===" % url)
			f = open("%s/%s.%s.txt" % (outputDir, proto, domain), "w")
			f.write("###############################\n")
			f.write("%s\n" % url)
			f.write("###############################\n")
			f.write("\n")
			f.write(r.text)
			f.close()
	except requests.exceptions.ConnectionError:
		pass
	except requests.exceptions.ReadTimeout:
		pass
	except UnicodeEncodeError:
		pass

	threadLimiter.release()

with open(inputFile) as f:
	for l in f:
		line = l.strip()
		for proto in protos:
			try:
				threading.Thread(target=getRobots, args=[proto, line]).start()
			except KeyboardInterrupt:
				print("\nKeyboard exit")
				os._exit(1)
			except Exception as e:
				print("")
				print(e)
				print("")
