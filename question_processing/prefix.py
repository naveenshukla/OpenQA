#!/usr/bin/python2.7 -tt

import urllib2
import sys
import json
import urllib
import ast

dir = ast.literal_eval(open('.config','r').read())['home']+'question_processing/'

def	get_json(query_string):
		url = insert(query_string)
		req = urllib2.Request(url, None, {'Accept':'application/json'})
		str_xml = urllib2.urlopen(req).read()
		return json.loads(str_xml)


def	insert(query_string):
		url = open(dir+'templates/prefix.template','rU').read()
		url = url.replace('{query_string}', query_string)
		return url


def	main():
		args = sys.argv[1:]
		if len(args) < 1:
			print('usage: ./prefix.py prefix')
			sys.exit(0)
		
		print(json.dumps(get_json(urllib.quote_plus(args[0])), sort_keys = True, indent = 4, separators = (',',': ')))


if __name__ == '__main__':
	main()
		
		
		
