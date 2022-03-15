from os import walk
from os.path import sep

from reddit_scraper.cc_lister import list_content_creators

def count_blanks(filename):
	count=0
	with open(filename) as rfile:
		for line in rfile.readlines():
			line=line.strip()
			if not line:
				count+=1
	return count

def find_blanks(cc):
	l=list()
	for x,y,filelist in walk(cc):
		for file in filelist:
			file=sep.join([x,file])
			c=count_blanks(file)
			if c > 3:
				l.append(file)
	return l

def find_all_blanks():
	d=dict()
	for cc in list_content_creators():
		d[cc]=find_blanks(cc)
	for x,y in d.items():
		print(x,y)

find_all_blanks()
