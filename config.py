#!/usr/bin/python2.7 -tt

import commands

hash = {}
(status, output) = commands.getstatusoutput('pwd')
if status == 0:
	home = output+'/'
hash['home'] = home
open('.config', 'w').write(str(hash))
(status1, output) = commands.getstatusoutput('cp .config question_classification/')
(status2, output) = commands.getstatusoutput('cp .config question_processing/')
(status3, output) = commands.getstatusoutput('cp .config question_processing/chunker/')
(status4, output) = commands.getstatusoutput('cp .config scripts/')
(status5, output) = commands.getstatusoutput('cp .config language_api/')
(status6, output) = commands.getstatusoutput('cp .config query_engine')
if status1 | status2 | status3 | status4 | status5 | status6  == 0:
	print('.config file created')

