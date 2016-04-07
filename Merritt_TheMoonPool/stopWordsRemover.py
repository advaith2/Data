#!/usr/bin/python2.7

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
from nltk import word_tokenize
import string
import re
import csv

#lemmatizing

wordlist =  []

def pos_tagging(input):
    details = pos_tag(word_tokenize(input))
    new_details = []
    for word, typ in details:
        if word == typ:
            continue
        elif typ in ['TO','SYM','RP','WDT','WP','PRP','PRP$','DT','UH','EX','IN','CC','LS',':','$','(',')','--','.',':','CC']:
            continue
        else:
            new_details.append(word+'<<'+typ+'>>')
    return new_details


def process_file():
    data = ''
    with open('TrialData/Merritt_TheMoonPool.txt','r') as f:
        for temp in f.readlines():
            temp = temp.replace('\r\n',' ')
            data = data + temp
    data = re.sub(' +',' ',data)
    data_list = sent_tokenize(data)
    with open("output.csv","wb") as f1:
        writer=csv.writer(f1)
        writer.writerow(['SENTENCE','DETAILS'])
        for lines in data_list:
            details = pos_tagging(lines)
            writer.writerow([lines,' '.join(details)])


def load_wordList():
    global wordlist
    with open('stop-words','r') as f:
        wordlist = [i.strip() for i in f.readlines()]
    wordlist=wordlist+stopwords.words('english')
    wordlist = wordlist

def print_word_list():
    for word in wordlist:
        print word+' ',

if __name__ == '__main__':
    load_wordList()
    process_file()
    #print_word_list()
