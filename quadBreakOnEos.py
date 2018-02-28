
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random

class Quadrigram:

	BOS = 'BOS'
	EOS = 'EOS'
	vocabulary = set()
	documents = {}

	def getBOSfromEOS(self, eosWord):
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		BOSesWithEOS = [ context for context in BOSes if eosWord in context ]
		#print 'eosword', eosWord
		#print 'BOS containing EOS', BOSesWithEOS
		if len(BOSesWithEOS) > 0:
			BOSesWithEOS = BOSesWithEOS[ random.randint(0, len(BOSesWithEOS)-1) ]
			print BOSesWithEOS
			return BOSesWithEOS
		return BOSes[ random.randint(0, len(BOSes)-1) ]

	def getRandomBOS(self):
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		return BOSes[ random.randint(0, len(BOSes)-1) ]

	def randomByContext(self, context):
		# TODO: check if can select word in better way that 'random'
		c = self.pc[context]
		possible = self.pc[context].keys()
		return possible[random.randint(0, len(possible)-1)]

	def generate(self, length=7, rows=2):
		modLength = length + random.randint(0,length / 2)
		sentence = []
		lastBOSword = 0
		r = 0
		l = 0
		while r < rows :
			lastBOSword += 1
			if len(sentence) == 0 or sentence[-1] == self.EOS:
				bosContext = self.getRandomBOS()
				sentence.append(bosContext[1])
				sentence.append(bosContext[2])
				predicted = self.randomByContext(bosContext)
			elif sentence[-1] == '\n':
				bosContext = self.getBOSfromEOS(sentence[-2])				
				#sentence.append(bosContext[1])
				sentence.append(bosContext[2])
				sentence.append(self.randomByContext(bosContext))
				predicted = self.randomByContext((bosContext[1], sentence[-2], sentence[-1]))
			else:
				predicted = self.randomByContext((sentence[-3], sentence[-2], sentence[-1]))

			sentence.append(predicted)
			if lastBOSword >= length and sentence[-1] in self.eosWords:
				sentence.append('\n')
				lastBOSword = 0
				r += 1
				continue

			if l >= modLength and False:
				sentence.append('\n')				
				lastBOSword = 0			
				r += 1
		l +=1
		return ' '.join(sentence)
	
	@classmethod
	def train(cls, vocabulary, documents):
		documents = documents[:]
		quadrigram = cls()
		quadrigram.eosWords = set()
		quadrigram.vocabulary = vocabulary
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

		quadrigram.eosWords.update([ eos[-1] for eos in  quadrigram.pc.keys() if cls.EOS in quadrigram.pc[eos] ])
		print quadrigram.eosWords
		return quadrigram
