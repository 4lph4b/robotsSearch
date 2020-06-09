#!/usr/bin/python

import requests
import sys

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

protos = ['http', 'https']
ports  = [80,443,8080,8443]

with open('webservers.txt') as f:
	for l in f:
		line = l.strip()

		for proto in protos:
			for port in ports:
				try:
					url = "%s://%s:%d/robots.txt" % (proto, line, port)
					sys.stdout.write("\033[K%s\r" % url)
					sys.stdout.flush()
					r = requests.get(url, verify=False, timeout=1)
					if r.status_code == 200:
						print("=== %s ===" % url)
						print(r.text)
						print()
				except:
					pass

print("\033[K=== Done! ===")
