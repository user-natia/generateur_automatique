#!/usr/bin/env python3
# coding=utf-8
import sys, zipfile, json, tempfile, os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('h5pfile', help='h5p file')
parser.add_argument('sentsfile', help='sentences file')
args = parser.parse_args()
h5pfilename = args.h5pfile
tmpfolder = tempfile.TemporaryDirectory()

print('Unzipping H5P file: '+h5pfilename)
with zipfile.ZipFile(h5pfilename) as h5pzipfile:
	h5pzipfile.extractall(tmpfolder.name)

	# Changing name of exercice
	with open(tmpfolder.name+'/h5p.json') as h5pfile:
		h5pjson = json.load(h5pfile)
		h5pjson['title'] = h5pjson['title']+' - generated'
		h5pfile.close()
		with open(tmpfolder.name+'/h5p.json', 'w') as h5pfile:
			json.dump(h5pjson, h5pfile)

	with open(tmpfolder.name+'/content/content.json') as contentfile:

		print('Opening json content')
		contentjson = json.load(contentfile)
		contentfile.close()

		print('Adding questions')
		questions = contentjson['questions']

		# ICI ON AJOUTE UNE OU PLUSIEURS (50) QUESTIONS DEPUIS LE CORPUS
		with open(args.sentsfile,'r') as sentsfile:
			for phrase in sentsfile:
				phrase = phrase.strip()
				print(phrase)
				questions.append(phrase)
					
		with open(tmpfolder.name+'/content/content.json', 'w') as contentfile:
			# print(contentjson)
			json.dump(contentjson, contentfile)
			contentfile.close()

			print('Zipping file')
			h5pfilenameout = h5pfilename[:-4]+'-generated'+'.h5p'
			with zipfile.ZipFile(h5pfilenameout, 'w') as h5pfilenameoutzip:
				for dirname, subdirs, files in os.walk(tmpfolder.name):
					# h5pfilenameout.write(dirname, os.path.relpath(dirname, tmpfolder.name))
					for filename in files:
						h5pfilenameoutzip.write(os.path.join(dirname, filename), os.path.relpath(os.path.join(dirname,filename), tmpfolder.name))
