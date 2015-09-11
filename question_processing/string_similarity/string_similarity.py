#!/usr/bin/python2.7 -tt

import commands
import sys
import ast

home = ast.literal_eval(open('.config', 'rU').read())['home'] 

def	calculate(ontology, keyword):
		output = commands.getoutput('java -cp '+home+'question_processing/string_similarity/ StringSimilarity '+ontology+' '+keyword).strip().strip('\n')
		return output


def	main():
		args = sys.argv[1:]
		if len(args) < 2:
			print('usage: ./string_similarity.py ontology keyword')
			sys.exit(0)
		
		calculate(args[0], args[1])


if __name__ == '__main__':
	main()
