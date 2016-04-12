#!/usr/bin/python2.7

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import string
import re
import csv

#lemmatizing

wordlist =  []

def getWordNetType(tag):
    if tag in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ
    elif tag in ['NN', 'NNS', 'NNP', 'NNPS','POS','FW']:
        return wn.NOUN
    elif tag in ['RB', 'RBR', 'RBS','WRB']:
        return wn.ADV
    elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    return wn.NOUN

def pos_tagging(input,flag_bit):
    wn_lem = WordNetLemmatizer()
    details = pos_tag(word_tokenize(input))
    new_details = []
    for word, typ in details:
        if word == typ:
            continue
        elif typ in ['TO','SYM','RP','WDT','WP','PRP','PRP$','DT','UH','EX','IN','CC','LS',':','$','(',')','--','.',':','CC','MD','CD','WP$','PDT']:
            continue
        else:
            word1 = wn_lem.lemmatize(unicode(word,errors='replace'),pos=getWordNetType(typ))
            if flag_bit ==1:
                new_details.append(word1+'<<'+typ+'>>')
            else:
                new_details.append(word1)
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
            details = pos_tagging(lines,1)
            writer.writerow([lines,' '.join(details)])

def process_fileV1():
    data = ''
    with open('TrialData/Merritt_TheMoonPool.txt','r') as f:
        for temp in f.readlines():
            temp = temp.replace('\r\n',' ')
            data = data + temp
    data = re.sub(' +',' ',data)
    data_list = sent_tokenize(data)
    with open('output.txt','w') as f2:
        for lines in data_list:
            details = pos_tagging(lines,0)
            f2.write(' '.join(details).encode('utf-8'))
            f2.write("\n")

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
    process_fileV1()
    #print_word_list()
