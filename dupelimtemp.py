# -*- coding: utf-8 -*-
from lxml import html
import urllib
import random
import sys
from bs4 import BeautifulSoup
f2 = open(sys.argv[1],"r+")
f4 = open("unmatched","w+")
f5 = open("words.txt.old","r")
words = f2.readlines()
allWords = f5.readlines()
f5.close()
print len(words)
writeFile = list()
for i in range(len(words)):
	word = words[i][:-1]
	if word not in writeFile: #duplicate elimination in "sys.argv" file
		writeFile.append(word)

writeFile.sort()
matched = list()
f2.close()
#f3 = open(sys.argv[1]+".old","w+")
for i in range(len(writeFile)):
	#print writeFile[i]
	r = urllib.urlopen('http://tureng.com/tr/turkce-ingilizce/' + writeFile[i]).read()
	soup = BeautifulSoup(r,"lxml")
	x = soup.find('h1').string.encode('utf-8')
	if x != writeFile[i]:
		f4.write(writeFile[i] +"\n") #unmatched
		print writeFile[i],x
	else:
#        f3.write(writeFile[i] + "\n") #matched
		matched.append(writeFile[i] + "\n")

f3 = open(sys.argv[1]+".old","w+")
random.shuffle(matched)
for i in matched:
	if i not in allWords:
		f3.write(i)
f3.close()

if len(sys.argv) > 2 and sys.argv[2] == "1":
	f3 = open(sys.argv[1]+".old","r+")
	f5 = open("words.txt.old","r")
	session = f3.readlines()
	total = f5.readlines()
	f5.close()
	f5 = open("words.txt.old","w")
	newtotal = sum([total],session)
	newtotal.sort()
	print len(newtotal)
	for i in newtotal:
		f5.write(i)
