#!/usr/bin/python2.7
from openpyxl import load_workbook
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import re

wordlist =  []

def openWorkBook():
    wb = load_workbook(filename = 'technovelgy.xlsx')
    ws = wb.active
    iterrows = iter(ws.rows)
    next(iterrows)
    for row in iterrows:
        if row[4].value:
            row[5].value = process_reference(row[4].value)
        else:
            row[5].value = ''
    wb.save('technovelgy_v1.xlsx')

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

def pos_tagging(input):
    wn_lem = WordNetLemmatizer()
    details = pos_tag(word_tokenize(input))
    new_details = []
    for word, typ in details:
        if word == typ:
            continue
        elif typ in ['TO','SYM','RP','WDT','WP','PRP','PRP$','DT','UH','EX','IN','CC','LS',':','$','(',')','--','.',':','CC','MD','CD','WP$','PDT']:
            continue
        elif word in ["'t","'ve","'d","'ll","'s","'m","'am","n't"]:
            continue
        else:
            word1 = wn_lem.lemmatize(word,pos=getWordNetType(typ))
            new_details.append(word1)
    return new_details

def process_reference(input):
    input = input.replace('\r\n',' ')
    #input = remove_dialogues(input)
    words = []
    sentences = sent_tokenize(input)
    for sentence in sentences:
        sentence = re.sub(r'[\.]+','',sentence)
        words.extend(pos_tagging(sentence))
    words = [x for x in words if x.lower() not in wordlist]
    return ' '.join(words)

def load_wordList():
    global wordlist
    with open('stop-words','r') as f:
        wordlist = [i.strip().lower() for i in f.readlines()]
    wordlist=wordlist+stopwords.words('english')
    wordlist = wordlist

def remove_dialogues(input):
    input = re.sub(r'\"(.+?)\"|\'(.+?)\'','',input)
    input = re.sub(r'[\.]+','.',input)
    input = re.sub(r' +',' ',input)
    return input

if __name__ == '__main__':
    load_wordList()
    openWorkBook()
