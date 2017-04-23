#!/usr/bin/python3 -tt


import sys

def	extract_class_hierarchy(lines, save):
		f_index = 1
		c_hash = {}
		for line in lines:
			c_class = line[:line.find(':')]
			f_class = line[line.find(':')+1: line.find(' ')]
			if c_hash.get(c_class) == None:
				f_hash = {}
				f_hash[f_class] = f_index
				f_index += 1
				c_hash[c_class] = f_hash
			else:
				f_hash = c_hash[c_class]
				f_hash[f_class] = f_index
				f_index += 1
				c_hash[c_class] = f_hash;	
		if save:
			open('svm_class_id_mapping', 'w').write(str(c_hash))
		return c_hash


			
def	coarse_filter(lines, megam):
		f = open('../data/training_data/'+megam+'coarse.train', 'w')
		for line in lines:
			f.write(line[:line.find(':')]+line[line.find(' '):])
		f.close()	


def	fine_filter(lines, coarse_classes, megam):
		file_handles = {}
		for coarse_class in coarse_classes.keys():
			file_handles[coarse_class] = open('../data/training_data/'+megam+'fine.'+coarse_class+'.train', 'w')
		
		for line in lines:
			coarse_class = line[:line.find(':')]
			file_handles[coarse_class].write(line[line.find(':')+1:])
			
	


def	readlines(filename):
		f = open(filename, 'rU', errors = 'ignore')
		lines = f.readlines()
		f.close()
		return lines


def	main():
		args = sys.argv[1:]
		if len(args) < 1:
			print('usage: ./make_training_files.py trec_source_file megam?')
			sys.exit(0)
		c_hash = extract_class_hierarchy(readlines(sys.argv[1]), False)
		lines = readlines(args[0])
		if len(args) > 1:
			coarse_filter(lines, 'megam/')
			fine_filter(lines, c_hash, 'megam/')
		else:
			coarse_filter(lines, '')
			fine_filter(lines, c_hash, '')
	


if __name__ == '__main__':
	main()		