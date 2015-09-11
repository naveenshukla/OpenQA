#!/usr/bin/python3 -tt

question_words = ['who','why','where','what','when','how','which','whose','whom', '?', '.', ':', ';', '"', '\'']


def	remove(text):
		text = text.lower().strip()
		if text in question_words:
			text = ''
		return text


def	main():
		print(remove(input()))


if __name__ == '__main__':
	main()
		
	
	
