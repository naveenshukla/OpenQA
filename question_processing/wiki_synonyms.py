#!/usr/bin/python2.7 -tt

import sys
import json
import urllib2
import ast

dir = ast.literal_eval(open('.config','rU').read())['home']+'question_processing/'

def	insert(term):
		req = open(dir+'templates/wiki_synonyms.template', 'rU').read()
		req = req.replace('{term}', term.replace(' ','%20'))

		return req


def	get_json(term):
		url = insert(term.strip())
		req = urllib2.Request(url, None,{'Accept':'application/json','X-Mashape-Key':'8Dov9eDJ3EmshMZPRLFAZoQ4WbX7p1M7vdJjsnCuLyqyL7v9WW'})
		try:
			str_json = urllib2.urlopen(req).read()
			_json =  json.loads(str_json)
		except:
			_json =  json.loads('{"http":404}')
	
		syn = []
		if _json['http'] == 200:
			terms = _json['terms']
			for term in terms:
				syn.append(term['term'])
			
		return syn
				


def	main():
		args = sys.argv[1:]
		if len(args) < 1:
			print('usage: ./wiki_synonyms.py term')
			sys.exit(0)
	

		print(get_json(args[0]))


if __name__ == '__main__':
	main()
		
		

