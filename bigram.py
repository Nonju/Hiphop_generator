
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

	@classmethod
	def train(cls, vocabulary, documents):
		bigram = cls()
		bigram.vocabulary = vocabulary
		bigram.documents = documents

		# determine context / word probabilities
		wordCount = {}
		for doc in documents:
			doc.insert(0, cls.BOS)
			doc.append(cls.EOS)

			for i in range(0, len(doc)-1):
				context = doc[i]
				word = doc[i+1]

				if context not in wordCount:
					wordCount[context] = {}

				if word not in wordCount[context]:
					wordCount[context][word] = 1
				else:
					wordCount[context][word] += 1

		# [
		# 	(('Sherlock'), { 'Holmes': 0.012, 'Mr.': 99.01 })
		# ]

		



		return bigram
