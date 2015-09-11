#!/usr/bin/python3 -tt

import sys

file = sys.argv[1]

lines = open(file, 'rU', errors='ignore').readlines()

starters = set()

for line in lines:
	line = line[line.find(' ')+1:]
	starters.add(line[:line.find(' ')].strip())


print(starters)


