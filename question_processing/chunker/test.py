import commands
(status, output) = commands.getstatusoutput('stanford-parser-full-2015-01-30/lexparser.sh'+' '+'.input.temp')
print status
print output