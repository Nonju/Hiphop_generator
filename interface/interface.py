
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os

import runapp
import updatevocab
from genius_lyrics_search import search

RUNNING = True

def placeholder():
	print 'not yet implemented'

def clearTerminal():
	os.system('clear')

def exit():
	global RUNNING
	RUNNING = False
	print 'Exiting app...'

menuOptions = [
	dict(name='Run app',       command='r', f=runapp.run),
	dict(name='Regather data', command='g', f=search.run),
	dict(name='Update vocab',  command='u', f=updatevocab.run),
	dict(name='Clear',         command='c', f=clearTerminal),
	dict(name='Quit',          command='q', f=exit)
]
def renderMenu():
	print '\nEnter a command to select an option:'
	for opt in menuOptions:
		if 'name' not in opt: continue
		if 'command' not in opt: continue

		print '- {} ({})'.format(opt['name'], opt['command'])

def handleSelection(command=''):
	def handleInvalidCommand():
		print 'Invalid command, try again'
	def getOptionByCommand():
		opt = filter(lambda x : x.get('command') == command, menuOptions)
		if not len(opt): return None
		return opt[0]

	if not command:
		handleInvalidCommand()
		return

	opt = getOptionByCommand()
	if opt is None:
		handleInvalidCommand()
		return

	# Run command
	opt['f']()

def run():
	while RUNNING:
		renderMenu()
		command = raw_input('> ')
		handleSelection(command=command)

