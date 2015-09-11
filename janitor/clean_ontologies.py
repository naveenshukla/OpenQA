#!/usr/bin/python2.7 -tt

import commands
import sys


print('[y|n] Are you sure you want to delete all the ontologies from /home/ontologies/ ')
sure1 = sys.stdin.readline().strip()
print('[y|n] Are you sure you want to delete all the ontologies from /home/ontologies/ ')
sure2 = sys.stdin.readline().strip()

if sure1.lower() == 'y' and sure2.lower() == 'y':
	(s, o) = commands.getstatusoutput('rm ../ontologies/*')

if s == 0:
	print('/home/ontologies/  -- All clean!')
