#!/usr/bin/python2.7 -tt

import sys
import nltk
import re
sys.path.append('chunker/')
# sys.path.append('./question_processing/')
# sys.path.append('./question_processing/string_similarity/')
# sys.path.append('./question_classification/')
# sys.path.append('./query_engine/')
# sys.path.append('./language_api')
import chunker as ques_chunk
# import classify as ques_classify
import spotlight
# import ontology
import json
import synonyms
import wiki_synonyms
import ast
import os
import io
import corpora_lookup
# import string_similarity
from difflib import SequenceMatcher
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
		print("question is : ")
		print question
		spot_keywords = {}
		index = 1
		confidence = 1.0
		repeat_list = []
		while confidence >= 0.1:
			req = insert(question.replace(' ','+'), str(confidence))
			json = get_json(req)
			print ("json is ")
			print (json)
			if json.get('Resources') != None:
				Resources = json['Resources']
				for Resource in Resources:
					if Resource['@surfaceForm'] in chunk_string and Resource['@URI'] not in repeat_list:
						resource_hash = {}
						resource_hash['url'] = Resource['@URI']
						url = resource_hash['url']
						url = url[:7] + 'live.' + url[7:]
						resource_hash['url'] = url
						print resource_hash['url']
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
	
		# if len(args) == 2:
			# req = insert(args[0].replace(' ','+'), args[1], '0', 'Default', 'Default', 'whitelist', '', '')
		# else:
			# req = insert(args[0].replace(' ','+'), args[1], args[2], args[3], args[4], args[5], args[6], args[7])
		# spot_keywords = {}
		# json = get_json(req)
		# json = json['annotation']
		# repeat_list = []
		# index = 0;
		# if json.get('surfaceForm')!=None:
		# 	surfaceForms = json['surfaceForm']
		# 	for surfaceForm in surfaceForms:
		# 		name = surfaceForm['@name']
		# 		# if name in chunk_string:
		# 		print surfaceForm['@name']
		# 		if surfaceForm.get('resource') != None:
		# 			resources = surfaceForm['resource']
		# 			for resource in resources:
		# 				if resource['@uri'] not in repeat_list:
		# 					resource_hash = {}
		# 					resource_hash['url'] = "http://live.dbpedia.org/resource/" + resource['@uri']
		# 					resource_hash['surfaceForm'] = name
		# 					resource_hash['types'] = resource['@types']
		# 					repeat_list.append(resource['@uri'])
		# 					spot_keywords[str(index)] = resource_hash
		# 					index += 1
		# print("chunk_string")
		# print chunk_string
		spot_keywords = {}
		index = 1
		confidence = 0
		repeat_list = []
		question = args[0]
		print("hey hey")
		req = insert(question.replace(' ','+'), str(confidence))
		json = get_json(req)
		json = json['annotation']
		if json.get('surfaceForm')!=None:
			surfaceForms = json['surfaceForm']
			for surfaceForm in surfaceForms:
				if surfaceForm.get('resource') != None:
					resources = surfaceForm['resource']
					for resource in resources:
						if resource['@uri'] not in repeat_list:
							resource_hash = {}
							resource_hash['url'] = "http://live.dbpedia.org/resource/" + resource['@uri']
							resource_hash['surfaceForm'] = surfaceForm['@name']
							resource_hash['types'] = resource['@types']
							repeat_list.append(resource['@uri'])
							spot_keywords[str(index)] = resource_hash
							index += 1
		print spot_keywords
if __name__ == '__main__':
	main()