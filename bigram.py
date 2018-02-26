
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

class Bigram:

	BOS = 'BOS'
	EOS = 'EOS'

	vocabulary = set()
	documents = {}

	def order(self):
		print 'Bigram'
		return 2

	def vocabulary(self):
		return self.vocabulary

	def freq(self, context, word):
		pass

	def total(self, context):
		pass

	def prob(self, context, word):
		pass

	def predict(self, context):
		c = self.pc[context]
		maxWord = self.EOS
		maxCount = 0
		for word, count in c.iteritems():
			if count > maxCount:
				maxCount = count
				maxWord = word

		return maxWord

	@classmethod
	def train(cls, vocabulary, documents):
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

		# [
		# 	(('Sherlock'), { 'Holmes': 0.012, 'Mr.': 99.01 })
		# ]

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
				# print 
				# print word
				# print count
				# print total
				# print  float(count) / float(total)
				bigram.pc[context][word] = float(count) / float(total)


		# print bigram.pc['here']

		return bigram
