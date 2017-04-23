#!/usr/bin/python2.7 -tt

import sys
import urllib2
import ast
import re

home = ast.literal_eval(open('.config','rU').read())['home']
dir = ast.literal_eval(open('.config','rU').read())['home']+'query_engine/'

def	insert(resource):
		# print ("in insert(resource) ")
		req = open(dir+'templates/ontology.template', 'rU').read()
		req = req.replace('{resource}', resource)
		# print ("in insert request")
		# print ("in insert resource")
		# print req
		return req


def	get_csv(resource):
		# print ("in get csv ")
		url = insert(resource.strip())
		# print ("url")
		# print url
		req = urllib2.Request(url, None,{'Accept':'text/csv'})
		str_csv = urllib2.urlopen(req).read()
		# print( " csv is this ")
		# print str_csv	
		return str_csv


def	isUrl(string):
		face = re.findall(r'http.*://.*/(\S+)', string)
		if len(face) == 1:
			face = face[0]
			return face
		else:
			return None

		
def	do_hash_ontology(resource):
		resource = resource.strip()
		# print("in do hash ontology")
		# print resource
		str_csv = get_csv(resource)
		print ( " str csv hahahahah ")
		print str_csv
		lines = str_csv.split('\n')
		lines = lines[1:-1]
		ontology_hash = {}
		for line in lines:
			if line == '':
				continue
			line_split = line.split(',')
			property = str(line_split[0][1:-1])
			proplen = len(line_split[0])
			val = line[proplen+1 : len(line)]
			if val and (val[0]=='"') : 
				val = val[1:]
			if val and (val[len(val)-1]=='"'):
				val = val[:len(val)-1]
			# print ( " property " + property + " value " + val)
			try:
				value = val
			except:
				value = '#'
			if value == '#':
				continue

			dbvalue = value
		
			dbvalues = []
			if property in ontology_hash.keys():
				dbvalues = ontology_hash[property]
				dbvalues.append(dbvalue)
			else:
				dbvalues = []
				dbvalues.append(dbvalue)
			
			ontology_hash[property] = dbvalues
		open(home+'ontologies/'+resource, 'w').write(str(ontology_hash))
		# print (" ontology has returned ")
		return ontology_hash


def	main():
		args = sys.argv[1:]
		if len(args) < 1:
			print('usage: ./ontology.py resource')
			sys.exit(0)
	
		do_hash_ontology(args[0])


if __name__ == '__main__':
	main()
