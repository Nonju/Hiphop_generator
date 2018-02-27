
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Entry point for Hip-hop generator app

Written using python2.7
"""

#import vocab
# from .models import bigram
# import codecs
# import json

# models
# import bigram
# import trigram
# import quadrigram

# def getDocuments(): # Remove
# 	#Replace with function that uses search
# 	with codecs.open('genius-lyrics-search/exampleoutput.json', 'r', encoding='utf8') as documents:
# 		return json.loads(documents.read())

# def getPart(docs, partName=''): # Remove
# 	parts = []
# 	for doc in docs:

# 		if partName not in doc['lyrics'].keys():
# 			continue

# 		for part in doc['lyrics'][partName]:
# 			parts.append(part)

# 	return parts

# def modelTrain(order=4): # Remove 
# 	voc = vocab.getVocab()
# 	docs = getDocuments()

# 	verseDocs = getPart(docs, partName=u'verse')
# 	# return bigram.Bigram.train(voc, verseDocs)

# 	if order == 2:
# 		return bigram.Bigram.train(voc, verseDocs)
# 	elif order == 3:
# 		return trigram.Trigram.train(voc, verseDocs)
# 	elif order == 4:
# 		return quadrigram.Quadrigram.train(voc, verseDocs)


from generate import generateLyrics

def main():

	testRows= 5
	order = None
	while not isinstance(order, int):
		order = raw_input('order: ')
		try: order = int(order)
		except: continue

	# model = modelTrain(order=order)
	while True:
		# generated = '\n'.join([ model.generate(length=20) for i in range(0, testRows) ])
		# print generated
		print generateLyrics(modelOrder=order)

		raw_input()

if __name__ == '__main__':
	main()
