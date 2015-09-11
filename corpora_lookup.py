#!/usr/bin/python2.7 -tt

import commands
import ast
import re
import sys

home = ast.literal_eval(open('.config', 'rU').read())['home']

def	find(keywords):
		keywords = keywords.replace(' ', '.*')
		keywords = '.*'+keywords+'.*'
		print('grep -h '+keywords+' '+home+'corpora/*')
		(status, output) = commands.getstatusoutput('grep -h '+keywords+' '+home+'corpora/*')
		
		lines = output.split('\n')
		clean_lines = []
		for line in lines:
			clean_lines.append(re.sub('[[0-9]*|([\s|\S]*)|@[\s|\S]+]', '', line)) 
		
		return clean_lines


def	main():
		print(find(sys.argv[1].strip()))


if __name__ == '__main__':
	main()
		
		
