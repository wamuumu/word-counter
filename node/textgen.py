from random import seed
from random import randint
from datetime import datetime
import operator

text = []
words = ["the","of","and","a","to","in","is","you","that","it","he","was","for","on","are","as","with","his","they","I","at","be","this","have","from","or","one","had","by","word","but","not","what","all","were","we","when","your","can","said","there","use","an","each","which","she","do","how","their","if","will","up","other","about","out","many","then","them","these","so","some","her","would","make","like","him","into","time","has","look","two","more","write","go","see","number","no","way","could","people","my","than","first","water","been","call","who","oil","its","now","find","long","down","day","did","get","come","made","may","part"]
sortedOccurrences = {}

def randomNumber(min, max):
	seed(datetime.now())
	return randint(min, max)

def generateTxt():
	global text
	rndLenght = randomNumber(200, 300)
	for i in range(rndLenght):
		rndInd = randomNumber(0, len(words)-1)
		text.append(words[rndInd])
	return ' '.join(text)

def calculateOccurrences():
	
	global sortedOccurences
	occurrences = {}

	for i in range(len(words)):
		occurrences[words[i]] = 0

	for i in range(len(text)):
		occurrences[text[i]] += 1

	sortedOccurences = dict( sorted(occurrences.items(), key=operator.itemgetter(1),reverse=True))

	return sortedOccurences

def topTenWords(name):
	topTen = []
	count = 0
	for key, value in sortedOccurences.items():
		tmp = {}
		tmp["word"] = key
		tmp["count"] = value
		tmp["occurrences"] = []
		tmp["occurrences"].append(name)
		topTen.append(tmp)
		count += 1
		if count == 10:
			break
	return topTen
