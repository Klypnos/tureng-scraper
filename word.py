# -*- coding: utf-8 -*-
from lxml import html
import urllib
from bs4 import BeautifulSoup
#page = requests.get("http://tureng.com/tr/turkce-ingilizce/strafe")
f2 = open("words","r+")
f = open("meanings","w")

words = f2.readlines()

for wordx in words:
    word = wordx[:-1]
    print word
    #print "http://tureng.com/tr/turkce-ingilizce/" + word
    f.write(word + ":\n")
    counter = 0
    r = urllib.urlopen('http://tureng.com/tr/turkce-ingilizce/' + word).read()
    soup = BeautifulSoup(r,"lxml")
    x = soup.find_all('td')
    for i in range(len(x)):
        if counter < 3 and x[i].a and x[i].a.string != word:
            counter += 1
            f.write("\t" + x[i].a.string.encode('utf-8') + "\n")
            print "\t" + x[i].a.string
