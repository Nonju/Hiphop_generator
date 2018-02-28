
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random

class Trigram:

	BOS = 'BOS'
	EOS = 'EOS'

	vocabulary = set()
	documents = {}

	def getRandomBOS(self):
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		return BOSes[ random.randint(0, len(BOSes) -1) ]

	def randomByContext(self, context):
		# TODO: check if can select word in better way that 'random'
		c = self.pc[context]
		possible = self.pc[context].keys()
		return possible[random.randint(0, len(possible)-1)]

	def generate(self, length=10, rows=10):
		sentence = []
		for i in range(0, length):
			if i == 0 or sentence[-1] == self.EOS:
				bosContext = self.getRandomBOS()
				sentence.append(bosContext[1])
				predicted = self.randomByContext(bosContext)
			else:
				predicted = self.randomByContext((sentence[-2], sentence[-1]))

			sentence.append(predicted)
		return ' '.join(sentence)

	@classmethod
	def train(cls, vocabulary, documents):
		documents = documents[:]
		trigram = cls()
		trigram.vocabulary = vocabulary
		trigram.documents = documents

		# determine context / word probabilities
		contextOccurrenceCount = {}
		for doc in documents:
			doc.insert(0, cls.BOS)
			doc.append(cls.EOS)

			for i in range(1, len(doc)-1):
				context = (doc[i-1], doc[i])
				word = doc[i+1]

				if context not in contextOccurrenceCount:
					contextOccurrenceCount[context] = {}

				if word not in contextOccurrenceCount[context]:
					contextOccurrenceCount[context][word] = 1
				else:
					contextOccurrenceCount[context][word] += 1

		def sumContextOccurences(context):
			s = 0
			for occurences, count in context.iteritems():
				s += count
			return s

		trigram.pc = {}
		for context, occurences in contextOccurrenceCount.iteritems():
			trigram.pc[context] = {}

			total = sumContextOccurences(contextOccurrenceCount[context])
			for word, count in occurences.iteritems():
				trigram.pc[context][word] = float(count) / float(total)

		return trigram
