#!/usr/bin/python2.7 -tt

import sys
import urllib2
import re
import ast

dir = ast.literal_eval(open('.config','rU').read())['home']+'query_engine/'

def	insert(resource, property, en):
		req = open(dir+'templates/rdf_query.template', 'rU').read()
		req = req.replace('{resource}', resource)
		req = req.replace('{property}',property)
		l = re.findall(r'({#(\S+)#})', req)
		if en:
			req = req.replace(l[0][0], l[0][1])
		else:
			req = req.replace(l[0][0], '')		

		return req


def	get_csv(resource, property, en):
		url = insert(resource.strip(), property.strip(), en)
		print(url)
		req = urllib2.Request(url, None,{'Accept':'text/csv'})
		str_csv = urllib2.urlopen(req).read()	
		return str_csv


def	main():
		args = sys.argv[1:]
		if len(args) < 2:
			print('usage: ./rdf_query.py resource property optional[lang=en]')
			sys.exit(0)
	
		if len(args) == 3:
			print(get_csv(args[0], args[1], True))
		else:
			print(get_csv(args[0], args[1], False))
		

if __name__ == '__main__':
	main()
