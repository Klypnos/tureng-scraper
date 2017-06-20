from lxml import html
import urllib
import sys
import os
from bs4 import BeautifulSoup
import random
import shutil
import signal

class Dictionary:
    safetoExit = True
    wordFileName = "words"
    dictFileName = "dictionary"
    def menu(self):
        exit = False
        while exit is False:
            print "\n################################################"
            print "\t#1 Duplicate Elimination"
            print "\t#2 Generate Meanings"
            print "\t## Any other key functions as exit"
            print "################################################\n"
            inp = raw_input()
            if inp == "1":
                self.eliminate()
            elif inp == "2":
                self.meanings()
            else:
                exit = True

    def meanings(self):
        #2 generate meanings file input: words
        self.wordFileName = raw_input("Input name of the word file (Press Enter for default:words):")
        if self.wordFileName == "": self.wordFileName = "words"
        wordFile = open(self.wordFileName, "r+")
        words = wordFile.readlines()
        meanings = open("meanings", "w")
        for i in words:
            word = i[:-1]
            print word
            meanings.write(word + ":\n")
            counter = 0
            #lookup tureng
            try:
                r = urllib.urlopen('http://tureng.com/tr/turkce-ingilizce/' + word).read()
            except:
                print "No internet connection."
                sys.exit()
            soup = BeautifulSoup(r,"lxml")
            x = soup.find_all('td')
            # write to meanings file
            for i in range(len(x)):
                if counter < 3 and x[i].a and x[i].a.string != word:
                    counter += 1
                    meanings.write("\t" + x[i].a.string.encode('utf-8') + "\n")
                    print "\t" + x[i].a.string


        return

    def eliminate(self):
        self.wordFileName = raw_input("Input name of the word file (Press Enter for default:words):")
        if self.wordFileName == "": self.wordFileName = "words"
        self.dictFileName = raw_input("Input name of the dictionary file (Press Enter for default:dictionary):")
        if self.dictFileName == "": self.dictFileName = "dictionary"
        #make a copy of words file
        shutil.copy2(self.wordFileName, self.wordFileName + ".copy")
        wordFile = open(self.wordFileName,"r+")
        words = wordFile.readlines()
        print "Length of new words (unfiltered): " + str(len(words))
        #search tureng if each word exists
        formatted = set() #word list in which typoes are eliminated
        for i in words:
            word = i[:-1] # eliminate new line feed
            try:
                r = urllib.urlopen('http://tureng.com/tr/turkce-ingilizce/' + word).read()
            except:
                os.remove(self.wordFileName + ".copy")
                print "No internet connection."
                sys.exit()
            soup = BeautifulSoup(r,"lxml")
            x = soup.find('h1').string.encode('utf-8')
             # x[i].a.string
            if x == word: # if they exist append to list
                formatted.add(word)
            else: # else they dont, print unmatched words
                y = soup.find("div", {"class": "clearfix"}).find_all("li")
                if len(y) > 0: #replace the word with the suggestion at the top
                    print word + " is replaced with " + y[0].a.string.encode('utf-8')
                    formatted.add( y[0].a.string.encode('utf-8') )
                else:
                    print word + " could not be replaced with any close word"
        # make a copy of dictionary file
        shutil.copy2(self.dictFileName, self.dictFileName + ".copy")
        dictFile = open(self.dictFileName, "r+")
        dictionaryList = dictFile.readlines()
        print "Length of dictionary (filtered): " + str(len(dictionaryList))
        dictionary = set()
        for i in dictionaryList:
            dictionary.add( i[:-1] )
        setCopy = set(dictionary)
        print "Length of new words (filtered): " + str(len( dictionary.difference(setCopy)))
        print "Length of dictionary (filtered): " + str(len(dictionary))
        # eliminate if they exist in the dictionary file
        wordList = list(formatted)
        for i in wordList:
            dictionary.add(i)
        self.safetoExit = False
        self.setToFile(dictionary.difference(setCopy),self.wordFileName,False)
        self.setToFile(dictionary,self.dictFileName,True)
        self.safetoExit = True
        os.remove( self.dictFileName + ".copy") #process is completed no need to keep copies
        os.remove( self.wordFileName + ".copy")
        return

    def safeExit(self,signum,frame):
        if self.safetoExit == True:
            print "Process halted."
            sys.exit()
        else: # revert files to the start of the program in case of a sigkill
            shutil.copy2(self.dictFileName + ".copy",self.dictFileName)
            shutil.copy2(self.wordFileName + ".copy",self.wordFileName)
            os.remove( self.dictFileName + ".copy")
            os.remove( self.wordFileName + ".copy")
            sys.exit()

    def setToFile(self,set,filename,sort):
        listed = list(set)
        if sort == True:
            listed.sort()
        file = open(filename,"w+")
        for i in listed:
            file.write(i + "\n")
        return


dictionary = Dictionary()
signal.signal(signal.SIGINT, dictionary.safeExit)
signal.signal(signal.SIGTERM, dictionary.safeExit)
dictionary.menu()
