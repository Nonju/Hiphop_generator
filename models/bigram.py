
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random

class Bigram:

	BOS = 'BOS'
	EOS = 'EOS'

	vocabulary = set()
	documents = {}

	def randomByContext(self, context):
		# TODO: check if can select word in better way that 'random'
		c = self.pc[context]
		possible = self.pc[context].keys()
		return possible[random.randint(0, len(possible)-1)]

	def generate(self, length=10):
		sentence = []
		for i in range(0, length):
			if i == 0 or sentence[-1] == self.EOS:
				predicted = self.randomByContext(self.BOS)
			else:
				predicted = self.randomByContext(sentence[i-1])

			sentence.append(predicted)
		return ' '.join(sentence)

	@classmethod
	def train(cls, vocabulary, documents):
		documents = documents[:]
		bigram = cls()
		bigram.vocabulary = vocabulary
		bigram.documents = documents

		# determine context / word probabilities
		contextOccurrenceCount = {}
		for doc in documents:
			doc.insert(0, cls.BOS)
			doc.append(cls.EOS)

			for i in range(0, len(doc)-1):
				context = doc[i]
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

		bigram.pc = {}
		for context, occurences in contextOccurrenceCount.iteritems():
			bigram.pc[context] = {}

			total = sumContextOccurences(contextOccurrenceCount[context])
			for word, count in occurences.iteritems():
				bigram.pc[context][word] = float(count) / float(total)

		return bigram
