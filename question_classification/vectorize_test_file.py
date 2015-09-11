#!/usr/bin/python3 -tt

import ast
import re
import sys

def	vectorize_lines(test_file_name):
		vectorize(open(test_file_name, 'rU', errors = 'ignore').readlines(), test_file_name)


def	vectorize(lines, test_file_name):
		f = open(test_file_name+'.vect', 'w')
		f1 = open('../util/word_index', 'rU')
		f1_lines = f1.readlines()
		word_id = int(f1_lines[0])
		word_index = {}
		word_index = ast.literal_eval(f1_lines[1])
		for line in lines:
			(vector_text, word_id) = vectorize_text(line, word_index, word_id)
			f.write('0 '+vector_text+'\n')

		f.close()


def	vectorize_text(text, word_index, word_id):
		index_freq = {}
		words = re.findall(r'(\S+)', text)
		for word in words:
			if word_index.get(word) == None:
				vector_word = word_id
				word_id += 1
			else:
				vector_word = word_index[word]

			if index_freq.get(vector_word) == None:
				index_freq[vector_word] = 1
			else:
				index_freq[vector_word] += 1
		
		tuples = sorted(index_freq.items(), key=first)
		line = ''
		for tuple in tuples:
			line += str(tuple[0])+':'+str(tuple[1])+' '

		return (line, word_id)


def	first(tuple):
		return tuple[0]


def	make_word_index(lines):
		word_index = {}
		id = 1
		for line in lines:
			line = line[line.find(' ')+1:]
			words = re.findall(r'(\S+)', line)
			for word in words:
				if word_index.get(word) == None:
					word_index[word] = id
					id += 1
				
		f = open('word_index', 'w')
		f.write(str(id+1)+'\n')
		f.write(str(word_index))
		
		return word_index
				
		
			
def	 main():
		args = sys.argv[1:]
		if len(args) != 1:
			print('usage: ./vectorize_test_file.py test_file')
			sys.exit(0)

		vectorize_lines(args[0])


if __name__ == '__main__':
	main()
	
		
