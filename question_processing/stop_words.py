#!/usr/bin/python3 -tt

from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")

def remove(text):
	text = ' '.join([word for word in text.split() if word not in cachedStopWords])
	return text

if __name__ == "__main__":
	print(remove(input()))
