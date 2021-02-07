#!/usr/bin/env python3
# coding=utf-8


#pour utiliser le module tabulé comme tsv
import csv
import re
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('tsv', help='input tsv file')
parser.add_argument('txt', help='output txt file with stars (blanks)')
parser.add_argument('-n','--number', help="number of sentences",type=int, default=20)
parser.add_argument('-mins','--minsize', help="minmum size of sentences",type=int, default=10)
parser.add_argument('-maxs','--maxsize', help="maximum size of sentences",type=int, default=20)
parser.add_argument('-pos','--posselect', help="maximum size of sentences",type=str, default=None)
parser.add_argument('-lem','--lemlst', help="maximum size of sentences",type=str, default=None)
args = parser.parse_args()
# print(args.number)

file = open(args.tsv)
reader = csv.reader(file, delimiter = '\t')

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	cleantext = cleantext.strip()
	return cleantext

def terminate(sents, outfile):
	print('Number of sentences: '+str(len(sents)))
	with open(outfile, 'w') as txtout:
		for sent in sents:
			txtout.write(sent+'\n')
	txtout.close()
	sys.exit(0)

len_phrase = 0 #taille de la phrase
starred = None
tokens = ''  #debut De la phrase
lemlst = None
if args.lemlst:
	lemlst = args.lemlst.split(',')

numbersent=0
sentsout = []
exit = False
for ligne in reader:
	if not exit:
		#print(ligne[0])
		#print(ligne[2])
		tk = ligne[0]
		lem = ligne[1][1:-1]
		if not starred:
			if args.posselect and ligne[2] == args.posselect:
				starred = True
				tk = '*' +tk+ '*'
			elif lemlst and lem in lemlst:
				starred = True
				tk = '*' +tk+ '*'
		tokens += tk+' '
		len_phrase	+= 1
		if ligne[2] == 'Punct' and lem in '.!?':
			if not args.posselect and not lemlst:
				starred = True
			if starred and (not args.minsize or args.minsize <= len_phrase) and (not args.maxsize or len_phrase <= args.maxsize) :
				if not args.number or len(sentsout) < args.number:
					sentsout.append(cleanhtml(tokens))
				else:
					terminate(sentsout, args.txt)
			len_phrase = 0 #taille de la phrase
			starred = None
			tokens = ''  #debut De la phrase

terminate(sentsout, args.txt)
