
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random

class Quadrigram:

	BOS = 'BOS'
	EOS = 'EOS'

	vocabulary = set()
	breakWords = set()
	documents = {}

	def getRandomBOS(self):
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		return BOSes[ random.randint(0, len(BOSes)-1) ]

	def randomByContext(self, context):
		# TODO: check if can select word in better way that 'random'
		c = self.pc[context]
		# possible = self.pc[context].keys()
		# return possible[random.randint(0, len(possible)-1)]
		maxValue = 0
		maxWord = ''
		for word in c:
			if self.pc[context][word] > maxValue:
				maxWord = word
		return maxWord

	def generate(self, length=10, minBreakLength=7):
		sentence = []
		cleanSentence = []
		wordsSinceBreak = 0
		for i in range(0, length):
			if i == 0 or sentence[-1] == self.EOS:
				bosContext = self.getRandomBOS()
				sentence.append(bosContext[1])
				sentence.append(bosContext[2])
				predicted = self.randomByContext(bosContext)
			else:
				predicted = self.randomByContext((sentence[-3], sentence[-2], sentence[-1]))

			sentence.append(predicted)
			cleanSentence.append(sentence[-1])
			wordsSinceBreak += 1			
			if sentence[-1] in self.breakWords and wordsSinceBreak >= minBreakLength:
				cleanSentence.append('\nBroke')
				wordsSinceBreak = 0

		return ' '.join(cleanSentence)

	@classmethod
	def train(cls, vocabulary, documents, bW):
		documents = documents[:]
		quadrigram = cls()
		quadrigram.vocabulary = vocabulary
		quadrigram.breakWords = bW
		quadrigram.documents = documents

		# determine context / word probabilities
		contextOccurrenceCount = {}
		for doc in documents:
			doc.insert(0, cls.BOS)
			doc.append(cls.EOS)

			for i in range(2, len(doc)-1):
				context = (doc[i-2], doc[i-1], doc[i])
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

		quadrigram.pc = {}
		for context, occurences in contextOccurrenceCount.iteritems():
			quadrigram.pc[context] = {}

			total = sumContextOccurences(contextOccurrenceCount[context])
			for word, count in occurences.iteritems():
				quadrigram.pc[context][word] = float(count) / float(total)

		return quadrigram
