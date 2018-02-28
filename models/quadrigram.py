
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random

class Quadrigram:

	BOS = 'BOS'
	EOS = 'EOS'
	vocabulary = set()
	invalidEndWords = set()
	invalidStartWords = set()
	documents = {}

	#Remove doubles of words
	def cleanSentence(self, sentence):
		cleanSentences = []

		punctuation = ['.', ',', '...', '\'', '-']

		while sentence[0] in punctuation:
			del sentence[0]

		for i in range(0, len(sentence)-1):
			cleanSentences.append(sentence[i])
			if sentence[i] == '\n':
				if sentence[i-1] == sentence[i+1]:
					del cleanSentences[-2]
			if sentence[i-1] == '\n':
				if sentence[i] in self.invalidStartWords:
					del cleanSentences[-1]
			if sentence[i] == self.EOS or sentence[i] == self.BOS:
				del cleanSentences[-1]

			if len(cleanSentences) > 2 and cleanSentences[-2] == '.':
				cleanSentences[-1] = u'{}{}'.format(cleanSentences[-1][0].upper(), cleanSentences[-1][1:])

			if sentence[i] == '-':
				del cleanSentences[-1]

			if len(cleanSentences) > 2 and sentence[i] in punctuation:
				merged = '{}{}'.format(cleanSentences[-2], cleanSentences[-1])
				cleanSentences[-2] = merged
				del cleanSentences[-1]

			if len(cleanSentences) > 2 and sentence[i][0] == '\'':
				merged = '{}{}'.format(cleanSentences[-2], cleanSentences[-1])
				cleanSentences[-2] = merged
				del cleanSentences[-1]

		if len(cleanSentences) > 0:
			cleanSentences[0] = u'{}{}'.format(cleanSentences[0][0].upper(), cleanSentences[0][1:])

		return cleanSentences

	def getBOSfromEOS(self, eosWord):
		# if eosWord in self.invalidStartWords: return []
		#Check if end word also exist in start words
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		EOSesInBOSes = [ bos for bos in BOSes if eosWord in bos ]
		if len(EOSesInBOSes) <= 0: return []

		#If contexts found choose a random one 
		key = EOSesInBOSes[ random.randint(0, len(EOSesInBOSes)-1) ]
		value = self.pc[key].keys()
		if len(value) > 1:
			# print value
			value[ random.randint(0, len(value)-1) ]
		sentence = value
		#Dont want to add first word but still have to search with it
		sentence.append(self.randomByContext((key[1], key[2], sentence[-1]))) 
		sentence.append(self.randomByContext((key[2], sentence[-2], sentence[-1])))
		if self.EOS in sentence:
			sentence[-1] = '\n'
		return sentence

	def getRandomBOS(self):
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		return BOSes[ random.randint(0, len(BOSes)-1) ]

	def getLessRandomBOS(self, word):
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		BOSes = [ context for context in self.pc.keys() if word in context ]

		if len(BOSes) <= 0: return None
		return BOSes[ random.randint(0, len(BOSes)-1) ]

	def randomByContext(self, context):
		# TODO: check if can select word in better way that 'random'
		c = self.pc[context]
		# possible = self.pc[context].keys()
		# return possible[random.randint(0, len(possible)-1)]
		maxWord = ''
		maxValue = 0
		for word in c:
			if self.pc[context][word] > 0:
				maxWord = word
				maxValue = self.pc[context][word]
		return maxWord

	def randomSentenceBOS(self, sentence, bosContext=None):
		if len(sentence) > 1 and bosContext == None:
			word = sentence[-1]
			if sentence[-1] != '\n':
				word = sentence[-2]
			boxContext = self.getLessRandomBOS(word)
		if bosContext == None:
			bosContext = self.getRandomBOS()
		sentence.append(bosContext[1])
		sentence.append(bosContext[2])
		predicted = self.randomByContext(bosContext)
		return sentence, predicted
	
	def illegalEnd(self, sentence):
		word = sentence[-2]
		del sentence[-2]	
		foundBOS = self.getBOSfromEOS(word)
		if len(foundBOS) > 0:
			# print 'end word', word
			sentence.append(word)
			sentence += foundBOS
		else:
			sentence, predicted = self.randomSentenceBOS(sentence)
			sentence.append(predicted)

		return sentence 

	def generate(self, length=7, rows=2):
		modLength = length + random.randint(0,length / 2)
		sentence = []
		lastBOSword = 0
		r = 0
		while r < rows :
			lastBOSword += 1
			if len(sentence) == 0 or sentence[-1] == self.EOS:
				if len(sentence) > 0 and sentence[-1] == self.EOS: del sentence[-1]
				sentence, predicted = self.randomSentenceBOS(sentence)
			elif sentence[-1] == '\n':
				if sentence[-2] in self.invalidEndWords:
					sentence = self.illegalEnd(sentence)				
					continue
				bosContext = self.getBOSfromEOS(sentence[-2])
				if len(bosContext) == 0:
					sentence, predicted = self.randomSentenceBOS(sentence)
				else:
					sentence += bosContext
					continue

			else:
				predicted = self.randomByContext((sentence[-3], sentence[-2], sentence[-1]))

			sentence.append(predicted)
			if lastBOSword >= length and sentence[-1] in self.eosWords:
				sentence.append('\n')
				lastBOSword = 0
				r += 1
				continue

			if lastBOSword >= modLength or False:
				sentence.append('\n')				
				lastBOSword = 0			
				r += 1
				continue
		sentence = self.cleanSentence(sentence)
		return ' '.join(sentence)
	
	@classmethod
	def train(cls, vocabulary, documents, invalidWords):
		documents = documents[:]
		quadrigram = cls()
		quadrigram.eosWords = set()
		quadrigram.bosWords = set()
		quadrigram.invalidEndWords = invalidWords['invalidEndWords']
		quadrigram.invalidStartWords = invalidWords['invalidStartWords']
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
		quadrigram.bosWords.update([ context for context in quadrigram.pc.keys() if cls.BOS in context ])
		return quadrigram
