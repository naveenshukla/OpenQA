#!/usr/bin/python3 -tt

import percepclassify
import nltk
import ast

home = ast.literal_eval(open('.config', 'rU').read())['home']

def	classify(question):
		question = preprocess(question)
		coarse_class = percepclassify.classify(question, percepclassify.get_g_hash_from_file(home+'data/models/coarse.model'))
		fine_class = percepclassify.classify(question, percepclassify.get_g_hash_from_file(home+'data/models/fine.'+coarse_class+'.model'))
		return coarse_class+':'+fine_class

def	preprocess(question):
		return ','.join(nltk.tokenize.word_tokenize(question)).replace(',',' ')

def	main():
		print(classify(input()))
	
if __name__ == '__main__':
	main()



		
