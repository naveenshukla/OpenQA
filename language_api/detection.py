#!/usr/bin/python2.7 -tt

import sys
import urllib2
import json
import ast

dir = ast.literal_eval(open('.config', 'rU').read())['home']+'language_api/'

def	insert(query):
		req = open(dir+'templates/detection.template', 'rU').read()
		req = req.replace('{query}', query)

		return req


def	get_json(query):
		query = query.replace(' ','+').strip()
		url = insert(query)
		req = urllib2.Request(url, None,{'Accept':'application/json'})
		str_json = urllib2.urlopen(req).read()	
		return json.loads(str_json)


def	main():
		args = sys.argv[1:]
		if len(args) < 1:
			print('usage: ./detection.py line')
			sys.exit(0)
		
		get_json(args[0])

if __name__ == '__main__':
	main()
