#!/usr/bin/python3 -tt

import sys
import random
import ast

home = ast.literal_eval(open('.config', 'rU').read())['home']

def	sample(class_hash):
		f_out = open(home+'data/sample_question.txt', 'w')
		for clazz in class_hash.keys():	
			list = class_hash[clazz]
			random.shuffle(list)
			f_out.write('## '+clazz+'\n')
			for i in range(5):
				if i < len(list):
					f_out.write(list[i])
		f_out.close()
			
			
def	group(class_hash, lines):
		for line in lines:
			clazz = line[:line.find(' ')]
			class_hash[clazz].append(line)
		
		return class_hash


def	init_hash(filename):
		f = open(filename, 'rU')
		class_hash = {}
		for line in f.readlines():
			class_hash[line[:line.find(' ')]] = []
		
		return class_hash


def	readlines(filename):
		return open(filename, 'rU', errors = 'ignore').readlines()


def	main():
		args = sys.argv[1:]
		if len(args) < 2:
			print('usage: ./sample_questions.py from_file with_classes ')
			sys.exit(0)

		sample(group(init_hash(args[1]), readlines(args[0])))


if __name__ == '__main__':
	main()	
		
			
		
