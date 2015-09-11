#!/usr/bin/python2.7 -tt
import commands
import sys

def	lang(value):
		return commands.getoutput('java -cp jsonic-1.2.0.jar: LangDetect '+value)


if __name__ == '__main__':
	print(lang(sys.argv[1].strip()))

