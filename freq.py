#!/usr/bin/env python3
# coding=utf-8


#frequence de mots :

import sys
import re

file = open("choupie1.txt", "r")
#content = file.read()

listV_counted = {}
tFaciles = []
faciles = []
difficiles = []
tDifficiles = []

#listVerbs = content.split()
#file.close()

for phrase in file:
	#print(phrase)
	matchV = re.search(r"\*(.*)\*",phrase)
	if matchV :
		#print("Verbs : " , matchV.group(1))
		verb=matchV.group(1)
		if verb in listV_counted:
			listV_counted[verb] += 1
		else:
			listV_counted[verb] = 1


listV_sorted = sorted(listV_counted.items(),key=lambda item: item[1],reverse=True)

for verb,count in listV_sorted:
	print(verb,count)

#avigo pirveli oci da gamoviyeno mxolod es oci, gadavakopiro pirveli 