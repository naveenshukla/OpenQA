#!/usr/bin/python2.7 -tt

import sys
import json
import urllib2
import ast

dir = ast.literal_eval(open('.config','rU').read())['home']+'question_processing/' 

def	insert(text, confidence, support='0', supporter='Default', disambiguator='Default', policy='whitelist', types='', sparql=''):
		req = open(dir+'templates/spotlight.template', 'rU').read()
		req = req.replace('{text}', text)
		req = req.replace('{confidence}', confidence)
		req = req.replace('{support}', support)
		req = req.replace('{supporter}', supporter)
		req = req.replace('{disambiguator}', disambiguator)
		req = req.replace('{policy}', policy)
		req = req.replace('{types}', types)
		req = req.replace('{sparql}', sparql)

		return req


def	get_json(url):
		req = urllib2.Request(url, None,{'Accept':'application/json'})
		str_json = urllib2.urlopen(req).read()
		return json.loads(str_json)


def	spot_keywords(question, chunk_string):
		spot_keywords = {}
		index = 1
		confidence = 1.0
		repeat_list = []
		while confidence >= 0.1:
			req = insert(question.replace(' ','+'), str(confidence))
			json = get_json(req)
			if json.get('Resources') != None:
				Resources = json['Resources']
				for Resource in Resources:
					if Resource['@surfaceForm'] in chunk_string and Resource['@URI'] not in repeat_list:
						resource_hash = {}
						resource_hash['url'] = Resource['@URI']
						resource_hash['types'] = Resource['@types']
						resource_hash['surfaceForm'] = Resource['@surfaceForm']
						spot_keywords[str(index)] = resource_hash
						index += 1
						repeat_list.append(Resource['@URI'])
			confidence -= 0.1

		return spot_keywords
					
			
		

def	main():
		args = sys.argv[1:]
		if len(args) < 2:
			print('usage: ./spotlight.py question confidence optional[support, supporter, disambiguator, policy, types, sparql]')
			sys.exit(0)
	
		if len(args) == 2:
			req = insert(args[0].replace(' ','+'), args[1], '0', 'Default', 'Default', 'whitelist', '', '')
		else:
			req = insert(args[0].replace(' ','+'), args[1], args[2], args[3], args[4], args[5], args[6], args[7])

		print(json.dumps(get_json(req), sort_keys=True, indent=4, separators=(',',': ')))


if __name__ == '__main__':
	main()
		
		

