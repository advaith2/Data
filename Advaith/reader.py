'''
Created on Apr 20, 2016

@author: Advaith GVK
'''

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import string
import csv
from fileinput import filename

corpusdir = 'C:/Users/Advaith GVK/workspace/Trial/src/Pack/New folder' # Directory of corpus.

newcorpus = PlaintextCorpusReader(corpusdir, '.*')

filenames = newcorpus.fileids()
# print newcorpus.sents()

def getWordNetType(tag):
        #print tag
        if tag in ['JJ', 'JJR', 'JJS']:
            return wn.ADJ
        elif tag in ['NN', 'NNS', 'NNP', 'NNPS','POS','FW']:
            return wn.NOUN
        elif tag in ['RB', 'RBR', 'RBS','WRB']:
            return wn.ADV
        elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            return wn.VERB
        return wn.NOUN


def returnstop(filename):
    from openpyxl import load_workbook
    wb = load_workbook(filename='C:/Users/Advaith GVK/workspace/Trial/src/Pack/tfidf-final.xlsx', read_only=True)
    name=filename.replace('.txt', '')
    name= name[:30]
    ws= wb[name]
    i=0
    for row in ws.rows:
        i=i+1
    table=[ [ 0 for i in range(3) ] for j in range(i) ]
    i=0
    for row in ws.rows:
        j=0
        for cell in row:
            table[i][j]=cell.value
            j=j+1
        i=i+1
    stop=[]
    length=int(0.75*i-1)
    for i in range(length):
        stop.append(table[i][0])
    stop=stop[1:]
    punctuat= list(string.punctuation)
    punctuat.append("--" )
    punctuat.append("``" )
    stop.append(punctuat)
    return stop


def lemm(tokens):
    new_tokens=[]
    pos=nltk.pos_tag(tokens, tagset=None)
    lem=WordNetLemmatizer()
    punctuat= list(string.punctuation)
    punctuat.append("--" )
    punctuat.append("``" )
    stop = stopwords.words('english') + punctuat
    stopterm=["''",'``',"us","'s","like","though","could","upon","within","came","saw","said", "..."]
    stop = stop + stopterm 
    for word,tag in pos:
        postag= getWordNetType(tag)
        word = lem.lemmatize(word, postag)
        if word not in stop:
            new_tokens.append(word)
    return new_tokens


sent_detector=nltk.data.load('tokenizers/punkt/english.pickle')
ofile=open("test.csv","w")
writer=csv.writer(ofile)
writer.writerow(['Sentence','Broken','Class'])
i=0
for filename in filenames:
    path=corpusdir+'/'+filename
    text=nltk.corpus.gutenberg.raw(path)
    sentences = sent_detector.tokenize(text.strip())
    stop=returnstop(filename)
    print stop
    for sent in sentences:    
        sent=sent.lower()
        sent.replace('\n', ' ')
        tokens=nltk.word_tokenize(sent)
        new_tokens=lemm(tokens)
        terms_all=[term for term in new_tokens if term not in stop]
        added = ' '.join(terms_all).encode('utf-8') 
        writer.writerow([sent,added," "])
    print filename
    i=i+1
print i