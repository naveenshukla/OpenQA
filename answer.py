#!/usr/bin/python2.7 -tt

import sys
import nltk
import re
sys.path.append('./question_processing/chunker/')
sys.path.append('./question_processing/')
sys.path.append('./question_processing/string_similarity/')
sys.path.append('./question_classification/')
sys.path.append('./query_engine/')
sys.path.append('./language_api')
import chunker as ques_chunk
import classify as ques_classify
import spotlight
import ontology
import json
import synonyms
import wiki_synonyms
import ast
import os
import io
import corpora_lookup
import string_similarity
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

home = ast.literal_eval(open('.config', 'r').read())['home']



def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def	pos_tag(ques, mother_hash):
		# print("in pos_tag\n")
		mother_hash['tag_sent'] = nltk.tag.pos_tag(nltk.tokenize.word_tokenize(ques))
		# print("in pos_tag, mother_hash --")
		# print(mother_hash)
		return mother_hash


def	classify(ques, mother_hash):
		mother_hash['ques_class'] = "LOC:other"
		return mother_hash


def	chunks(ques, mother_hash):
		# print("in chunks--")
		chunks = ques_chunk.get_chunks(ques)	
		mother_hash['ques_chunks'] = chunks 
		mother_hash['num_ques_chunks'] = len(chunks)
		return mother_hash


def	spot_keywords(ques, mother_hash):
		# print("in spot keywords ")
		h = spotlight.spot_keywords(ques, ','.join(mother_hash['ques_chunks'].values()).replace(',',' '))
		# print (" spot keywords ")
		# print h
		mother_hash['spot_keywords'] = h
		return mother_hash
		

def	get_ontology(resource):
		# print (" in get onotlogy ")
		# print resource
		if resource in os.listdir(home+'ontologies/'):
			try:
				ontology_hash = ast.literal_eval(io.open(home+'ontologies/'+resource, 'rU', encoding='latin-1').read())
			except:	
				ontology_hash = ontology.do_hash_ontology(resource)			
		else:
			ontology_hash = ontology.do_hash_ontology(resource)
		return ontology_hash


def	extract_resource(url):
		# print("In extract_resource ")
		r = re.findall(r'http.*://.*/(\S+)', url)
		# print(r)
		# print("Out extract resource")
		if len(r) >= 1:
			return r[0]
		else:
			return None


def	one_node_mayday(mother_hash):
		answer_hash = {}
		if mother_hash['num_ques_chunks'] == 1:
			keyword = mother_hash['ques_chunks']['1']
			re_keyword = None
			if len(wiki_synonyms.get_json(keyword)) >= 1:
				re_keyword = wiki_synonyms.get_json(keyword)[0]
				mother_hash = create_mother(re_keyword.replace(' ','_'))
				answer_hash = get_answer_hash(mother_hash)
			
			if len(answer_hash.keys()) == 0:
				if re_keyword:
					answer_hash['1_mayday']=corpora_lookup.find(re_keyword)
				else:
					answer_hash['1_mayday']=corpora_lookup.find(keyword)


		return answer_hash
			

def	collect_resource_information(ontology, in_hash={}):
		# in_hash['comment'] = ontology.get('http://www.w3.org/2000/01/rdf-schema#comment')
		in_hash['thumbnail'] = ontology.get('http://live.dbpedia.org/ontology/thumbnail')	
		in_hash['label']	 = ontology.get('http://www.w3.org/2000/01/rdf-schema#label')
		in_hash['name'] = ontology.get('http://live.dbpedia.org/property/name')	
		in_hash['homepage'] = ontology.get('http://xmlns.com/foaf/0.1/homepage')	
		in_hash['wiki_page_url'] = ontology.get('http://xmlns.com/foaf/0.1/isPrimaryTopicOf')	
		in_hash['birthDate'] = ontology.get('http://live.dbpedia.org/ontology/birthDate')
		in_hash['deathDate'] = ontology.get('http://live.dbpedia.org/ontology/deathDate')	
		in_hash['areaTotal'] = ontology.get('http://live.dbpedia.org/ontology/PopulatedPlace/areaTotal')	
		in_hash['anthem'] = ontology.get('http://live.dbpedia.org/ontology/anthem')	
		in_hash['capital'] = ontology.get('http://live.dbpedia.org/ontology/capital')	
		in_hash['leaderTitle'] = ontology.get('http://live.dbpedia.org/property/leaderTitle')
		in_hash['length'] = ontology.get('http://live.dbpedia.org/property/length')
		if in_hash.get('leaderTitle') == None:
			in_hash['leaderTitle'] = ontology.get('http://live.dbpedia.org/ontology/leaderTitle')
		in_hash['leaderName'] = ontology.get('http://live.dbpedia.org/property/leaderName')	
		if in_hash.get('leaderName') == None:
			in_hash['leaderName'] = ontology.get('http://live.dbpedia.org/ontology/leaderName')
		in_hash['leader'] = ontology.get('http://live.dbpedia.org/ontology/leader')	
		if in_hash.get('leader') == None:
			in_hash['leader'] = ontology.get('http://live.dbpedia.org/property/leader')
		in_hash['currency'] = ontology.get('http://live.dbpedia.org/property/currency')	
		in_hash['url'] = ontology.get('http://live.dbpedia.org/property/url')	
		in_hash['country'] = ontology.get('http://live.dbpedia.org/ontology/country')	
		in_hash['occupation'] = ontology.get('http://live.dbpedia.org/ontology/occupation')	
		in_hash['spouse'] = ontology.get('http://live.dbpedia.org/ontology/spouse')	
		in_hash['networth'] = ontology.get('http://live.dbpedia.org/ontology/networth')	
		in_hash['locationCity'] = ontology.get('http://live.dbpedia.org/ontology/locationCity')	
		in_hash['location'] = ontology.get('http://live.dbpedia.org/ontology/location')
		in_hash['revenue'] = ontology.get('http://live.dbpedia.org/ontology/revenue')	
		in_hash['author'] = ontology.get('http://live.dbpedia.org/property/author')	
		in_hash['runtime'] = ontology.get('http://live.dbpedia.org/property/Work/runtime')	
		in_hash['cinematography'] = ontology.get('http://live.dbpedia.org/ontology/cinematography')	
		in_hash['director'] = ontology.get('http://live.dbpedia.org/ontology/director')	
		in_hash['distributor'] = ontology.get('http://live.dbpedia.org/ontology/distributor')	
		in_hash['editing'] = ontology.get('http://live.dbpedia.org/ontology/editing')	
		in_hash['producer'] = ontology.get('http://live.dbpedia.org/ontology/producer')	
		in_hash['starring'] = ontology.get('http://live.dbpedia.org/ontology/starring')	
		in_hash['foundedBy'] = ontology.get('http://live.dbpedia.org/ontology/foundedBy')	
		in_hash['numberOfEmployees'] = ontology.get('http://live.dbpedia.org/ontology/numberOfEmployees')	
		in_hash['founder'] = ontology.get('http://live.dbpedia.org/ontology/founder')	
		in_hash['facultySize'] = ontology.get('http://live.dbpedia.org/ontology/facultySize')	
		in_hash['numberOfStudents'] = ontology.get('http://live.dbpedia.org/ontology/numberOf/Students')	
		return in_hash
	

def	one_node(mother_hash):
		# print("In one_node --")
		answer_hash = {}
		chunk_1 = mother_hash['ques_chunks']['1']
		if len(mother_hash['spot_keywords'].keys()) > 0:
			#http://dbpedia.org/resource/FIFA
			keyword1 = mother_hash['spot_keywords']['1']
			#FIFA
			resource1 = extract_resource(keyword1['url'])
			# print(" in one_node resource1 : ")
			# print(resource1)
			#ontology
			ontology1 = get_ontology(resource1)
			"""
			collect information from ontology
			"""
			
			hash_1 = {}
			hash_1 = collect_resource_information(ontology1, hash_1)

			answer_hash['1'] = hash_1

		return answer_hash


def	collect_answer(ontology_dict , matching_ontology, in_hash= {}):
		answer = {}
		for ontologies in ontology_dict.keys():
			ontology = ontology_dict[ontologies]
			# print (" machin ontogs")
			term  = matching_ontology[1]
			if term in ontology_dict[ontologies]:
					answer[str(ontologies)] = ontology[term]
		in_hash = {}
		print (" answer is ")
		print answer
		return in_hash


def	first(tuple):
		return tuple[0]


def	two_node(mother_hash):

		answer_hash = {}
		score_dict = {}
		ontology_dict  = {}
		for i in range(1,  len(mother_hash['spot_keywords']) + 1):	
			resource1 = extract_resource(mother_hash['spot_keywords'][str(i)]['url'])
			chunk1 = mother_hash['ques_chunks']['1']
			chunk2 = mother_hash['ques_chunks']['2']
			s1 = similar(chunk1, resource1)
			s2 = similar(chunk2, resource1)
			if s1 > s2:
				keyword1 = chunk2
			else:
				keyword1 = chunk1
			# print (" before ontology1 ")
			# print resource1
			ontology1 = {}
			# print(" after ontology1 ")
			if is_ascii(resource1):
				ontology1 = get_ontology(resource1)
				ontology_dict[resource1] = get_ontology(resource1)
				# print (" ontology dictionary ")
				# print ontology_dict[resource1]
			else: 
				continue
			hash_1 = {}
			hash_1 = collect_resource_information(ontology1, hash_1)
			synonyms_keyword_1 = synonyms.get_synonyms(keyword1)
			# print(" synonyms of ")
			# print(keyword1)
			# print (synonyms_keyword_1)
			synonyms_keyword_1.insert(0,keyword1)
			for syn in synonyms_keyword_1:
				flag = 0
				for onto_key in ontology1.keys():
					try:
						st = onto_key.split('/')
						score = float(similar(st[-1], syn))
						# print ( " st and syn ")
						# print st[-1]
						# print syn
					except:
						score = 0
					if score_dict.get(score) == None:
						score_dict[score] = onto_key
		matching_ontologies = sorted(score_dict.items(), reverse=True, key=first)[:5]
		# print (" maa chudao ")
		# print len(matching_ontologies)
		print matching_ontologies
		matching_ontologies = matching_ontologies[0]				
		hash_2 = {}
		hash_2 = collect_answer(ontology_dict, matching_ontologies, hash_2)
		print matching_ontologies
		print hash_2
		return answer_hash


def	get_answer_hash(mother_hash):
		answer_hash = None
		answer_hash = two_node(mother_hash)
		return answer_hash
			

def	create_mother(ques):
		# print("in create_mother--\n")
		mother_hash = {}
		mother_hash['ques'] = ques
		# print("calling pos_tag")
		mother_hash = pos_tag(ques, mother_hash)
		mother_hash = classify(ques, mother_hash)
		mother_hash = chunks(ques, mother_hash)
		# print("chunks\n")
		# print(mother_hash)
		mother_hash = spot_keywords(ques, mother_hash)
		
		return mother_hash

	
def	main():
		args = sys.argv[1:]
		if len(args) < 1:	
			print('usage: ./answer.py question')
			sys.exit(0)

		ques = args[0].strip()
		# print("in main, ques : " + ques)
		# print("calling create_mother")
		mother_hash = create_mother(ques)
		# print("in main, mother_hash --")
		# print(mother_hash)
		# print("in min, mother_hash : " + mother_hash)
		answer_hash = get_answer_hash(mother_hash)
		# print("in main, answer_hash : " + answer_hash)
		print('##question_hash##')
		# print(json.dumps(mother_hash, sort_keys=True, indent=4, separators=(',',': ')))
		print('##answer_hash##')
		#print(jd.raw_decode(answer_hash, sort_keys=True, indent=4, separators=(',',': ')))
		print(answer_hash)
		

if __name__ == '__main__':
	# print('calling main')
	main()
	
		

