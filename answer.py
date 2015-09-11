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


home = ast.literal_eval(open('.config', 'r').read())['home']

def	pos_tag(ques, mother_hash):
		mother_hash['tag_sent'] = nltk.tag.pos_tag(nltk.tokenize.word_tokenize(ques))
		return mother_hash


def	classify(ques, mother_hash):
		mother_hash['ques_class'] = ques_classify.classify(ques)
		return mother_hash


def	chunks(ques, mother_hash):
		chunks = ques_chunk.get_chunks(ques)	
		mother_hash['ques_chunks'] = chunks 
		mother_hash['num_ques_chunks'] = len(chunks)
		return mother_hash


def	spot_keywords(ques, mother_hash):
		h = spotlight.spot_keywords(ques, ','.join(mother_hash['ques_chunks'].values()).replace(',',' '))
		mother_hash['spot_keywords'] = h
		return mother_hash
		

def	get_ontology(resource):
		if resource in os.listdir(home+'ontologies/'):
			try:
				ontology_hash = ast.literal_eval(io.open(home+'ontologies/'+resource, 'rU', encoding='latin-1').read())
			except:	
				ontology_hash = ontology.do_hash_ontology(resource)			
		else:
			ontology_hash = ontology.do_hash_ontology(resource)
		return ontology_hash


def	extract_resource(url):
		r = re.findall(r'http.*://.*/(\S+)', url)
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
		in_hash['comment'] = ontology.get('http://www.w3.org/2000/01/rdf-schema#comment')
		in_hash['thumbnail'] = ontology.get('http://dbpedia.org/ontology/thumbnail')	
		in_hash['label']	 = ontology.get('http://www.w3.org/2000/01/rdf-schema#label')
		in_hash['name'] = ontology.get('http://dbpedia.org/property/name')	
		in_hash['homepage'] = ontology.get('http://xmlns.com/foaf/0.1/homepage')	
		in_hash['wiki_page_url'] = ontology.get('http://xmlns.com/foaf/0.1/isPrimaryTopicOf')	
		in_hash['birthDate'] = ontology.get('http://dbpedia.org/ontology/birthDate')
		in_hash['deathDate'] = ontology.get('http://dbpedia.org/ontology/deathDate')	
		in_hash['areaTotal'] = ontology.get('http://dbpedia.org/ontology/PopulatedPlace/areaTotal')	
		in_hash['anthem'] = ontology.get('http://dbpedia.org/ontology/anthem')	
		in_hash['capital'] = ontology.get('http://dbpedia.org/ontology/capital')	
		in_hash['leaderTitle'] = ontology.get('http://dbpedia.org/property/leaderTitle')
		if in_hash.get('leaderTitle') == None:
			in_hash['leaderTitle'] = ontology.get('http://dbpedia.org/ontology/leaderTitle')
		in_hash['leaderName'] = ontology.get('http://dbpedia.org/property/leaderName')	
		if in_hash.get('leaderName') == None:
			in_hash['leaderName'] = ontology.get('http://dbpedia.org/ontology/leaderName')
		in_hash['leader'] = ontology.get('http://dbpedia.org/ontology/leader')	
		if in_hash.get('leader') == None:
			in_hash['leader'] = ontology.get('http://dbpedia.org/property/leader')
		in_hash['currency'] = ontology.get('http://dbpedia.org/property/currency')	
		in_hash['url'] = ontology.get('http://dbpedia.org/property/url')	
		in_hash['country'] = ontology.get('http://dbpedia.org/ontology/country')	
		in_hash['occupation'] = ontology.get('http://dbpedia.org/ontology/occupation')	
		in_hash['spouse'] = ontology.get('http://dbpedia.org/ontology/spouse')	
		in_hash['networth'] = ontology.get('http://dbpedia.org/ontology/networth')	
		in_hash['locationCity'] = ontology.get('http://dbpedia.org/ontology/locationCity')	
		in_hash['revenue'] = ontology.get('http://dbpedia.org/ontology/revenue')	
		in_hash['author'] = ontology.get('http://dbpedia.org/property/author')	
		in_hash['runtime'] = ontology.get('http://dbpedia.org/property/Work/runtime')	
		in_hash['cinematography'] = ontology.get('http://dbpedia.org/ontology/cinematography')	
		in_hash['director'] = ontology.get('http://dbpedia.org/ontology/direector')	
		in_hash['distributor'] = ontology.get('http://dbpedia.org/ontology/distributor')	
		in_hash['editing'] = ontology.get('http://dbpedia.org/ontology/editing')	
		in_hash['producer'] = ontology.get('http://dbpedia.org/ontology/producer')	
		in_hash['starring'] = ontology.get('http://dbpedia.org/ontology/starring')	
		in_hash['foundedBy'] = ontology.get('http://dbpedia.org/ontology/foundedBy')	
		in_hash['numberOfEmployees'] = ontology.get('http://dbpedia.org/ontology/numberOfEmployees')	
		in_hash['founder'] = ontology.get('http://dbpedia.org/ontology/founder')	
		in_hash['facultySize'] = ontology.get('http://dbpedia.org/ontology/facultySize')	
		in_hash['numberOfStudents'] = ontology.get('http://dbpedia.org/ontology/numberOf/Students')	
		return in_hash
	

def	one_node(mother_hash):
		answer_hash = {}
		chunk_1 = mother_hash['ques_chunks']['1']
		if len(mother_hash['spot_keywords'].keys()) > 0:
			#http://dbpedia.org/resource/FIFA
			keyword1 = mother_hash['spot_keywords']['1']
			#FIFA
			resource1 = extract_resource(keyword1['url'])
			#ontology
			ontology1 = get_ontology(resource1)
			
			"""
			collect information from ontology
			"""
			
			hash_1 = {}
			hash_1 = collect_resource_information(ontology1, hash_1)

			answer_hash['1'] = hash_1

		return answer_hash


def	collect_answer(ontology, matching_ontologies, in_hash= {}):
		for term in matching_ontologies:
			onto = term[1]
			in_hash[extract_resource(onto)] = ontology[onto]
		
		return in_hash
		
		
def	first(tuple):
		return tuple[0]


def	two_node(mother_hash):
		answer_hash = {}
		#		
		resource1 = extract_resource(mother_hash['spot_keywords']['1']['url'])
		#iif len(mother_hash['spot_keywords'].keys()) > 1:
			#keyword1 = extract_resource(mother_hash['spot_keywords']['2']['url'])
		#else:
		chunk1 = mother_hash['ques_chunks']['1']
		chunk2 = mother_hash['ques_chunks']['2']
		s1 = string_similarity.calculate(chunk1, resource1)
		s2 = string_similarity.calculate(chunk2, resource1)
		
		if s1 > s2:
			keyword1 = chunk2
		else:
			keyword1 = chunk1
			
		ontology1 = get_ontology(resource1)
		
		"""
		collection generic information from ontology
		"""
		hash_1 = {}
		hash_1 = collect_resource_information(ontology1, hash_1)
			
		"""
		get the answer
		"""
		synonyms_keyword_1 = synonyms.get_synonyms(keyword1)
		synonyms_keyword_1.insert(0,keyword1)
		score_dict = {}


		
		print(len(ontology1.keys()) * len(synonyms_keyword_1) )
		for syn in synonyms_keyword_1:
			sum = 0
			index = 1
			for onto_key in ontology1.keys():
				if index >= 50:
					break;
				else:
					index += 1
				try:
					score = float(string_similarity.calculate(extract_resource(onto_key), syn))	
				except:
					score = 0
				if score_dict.get(score) == None:
					score_dict[score] = onto_key
				if score >= 90.0:
					sum += 1	
				if sum >= 2:
					break
				
		#find top 5 similarities:
		matching_ontologies = sorted(score_dict.items(), reverse=True, key=first)[:5]

		"""
		collect answer
		"""							
		hash_2 = {}
		hash_2 = collect_answer(ontology1, matching_ontologies, hash_2)
		print(hash_2)	
		"""
		collect resource information for answer
		"""	
		hash_3 = {}
		primary_answer = hash_2.items()[0][1]
		print(primary_answer)
		if extract_resource(primary_answer[0]) != None:
			hash_3 = collect_resource_information(get_ontology(extract_resource(primary_answer[0])), hash_3)

		answer_hash = {'1':hash_1, '2':hash_2, '3':hash_3}

		return answer_hash


def	get_answer_hash(mother_hash):
		answer_hash = None
		if len(mother_hash['spot_keywords'].keys()) == 1:
			answer_hash = one_node(mother_hash)
	
		if len(mother_hash['spot_keywords'].keys()) == 2:
			answer_hash = two_node(mother_hash)

		return answer_hash
			

def	create_mother(ques):
		mother_hash = {}
		mother_hash['ques'] = ques
		mother_hash = pos_tag(ques, mother_hash)
		mother_hash = classify(ques, mother_hash)
		mother_hash = chunks(ques, mother_hash)
		mother_hash = spot_keywords(ques, mother_hash)
		
		return mother_hash

	
def	main():
		args = sys.argv[1:]
		if len(args) < 1:	
			print('usage: ./answer.py question')
			sys.exit(0)

		ques = args[0].strip()
		mother_hash = create_mother(ques)
		answer_hash = get_answer_hash(mother_hash)
		print('##question_hash##')
		print(json.dumps(mother_hash, sort_keys=True, indent=4, separators=(',',': ')))
		print('##answer_hash##')
		#print(jd.raw_decode(answer_hash, sort_keys=True, indent=4, separators=(',',': ')))
		print(answer_hash)
		

if __name__ == '__main__':
	main()
	
		

