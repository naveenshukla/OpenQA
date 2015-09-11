#!/usr/bin/python2.7 -tt

import sys
import urllib2
import re
import ast

dir = ast.literal_eval(open('.config','rU').read())['home']+'question_processing/'


def	insert(term):
		req = open(dir+'templates/synonyms.template', 'rU').read()
		req = req.replace('{term}', term.replace(' ','+'))

		return req


def	get_synonyms(term):
		url = insert(term.strip())
		req = urllib2.Request(url, None,{'Accept':'application/html'})
		try:
			str_html = urllib2.urlopen(req).read()	
			return re.findall(r'<span class="text">([\w\s*\w*\s*\w*]+)</span>', re.findall(r'<div.*class="relevancy-list">([\s|\S]+)</div>[\s|\S]*<div id="filter-0"></div>', str_html)[0])
		except:
			return []


def	main():
		args = sys.argv[1:]
		if len(args) < 1:
			print('usage: ./synonyms.py term')
			sys.exit(0)
	
		print(get_synonyms(args[0]))


if __name__ == '__main__':
	main()
		
		

