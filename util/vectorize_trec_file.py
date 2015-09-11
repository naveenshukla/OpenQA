#!/usr/bin/python3 -tt

import make_training_files
import ast
import re
import sys


def	vectorize_lines(trec_file_name):
		vectorize(open(trec_file_name, 'rU', errors = 'ignore').readlines(), trec_file_name)


def	vectorize(lines, trec_file_name):
		f = open(trec_file_name+'.vect', 'w')
		word_index = make_word_index(lines)
		c_hash = make_training_files.extract_class_hierarchy(lines, True)
		coarse_index = 1
		coarse_class_hash = {}
		for line in lines:
			coarse_class = line[:line.find(':')]
			fine_class = line[line.find(':')+1:line.find(' ')]
			text = line[line.find(' ')+1:]
			if coarse_class_hash.get(coarse_class) == None:
				coarse_class_hash[coarse_class] = coarse_index
				coarse_index += 1
			vector_text = vectorize_text(text, word_index)
			vector_line = str(coarse_class_hash[coarse_class])+':'+str(c_hash[coarse_class][fine_class])+' '+vector_text
			f.write(vector_line+'\n')

		open('coarse_class_mapping', 'w').write(str(coarse_class_hash))
		f.close()


def	vectorize_text(text, word_index):
		index_freq = {}
		words = re.findall(r'(\S+)', text)
		for word in words:
			if index_freq.get(word_index[word]) == None:
				index_freq[word_index[word]] = 1
			else:
				index_freq[word_index[word]] += 1
		
		tuples = sorted(index_freq.items(), key=first)
		line = ''
		for tuple in tuples:
			line += str(tuple[0])+':'+str(tuple[1])+' '

		return line


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
			print('usage: ./vectorize_trec_file.py trec_file')
			sys.exit(0)

		vectorize_lines(args[0])


if __name__ == '__main__':
	main()
	
		
