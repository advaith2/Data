'''
Created on Apr 4, 2016

@author: Advaith GVK
'''
#import textmining
import nltk
from collections import Counter
import string
from nltk.corpus import stopwords
import nltk.data
from nltk.corpus import brown
#import nltk.tokenize.punkt as pk
import csv
path="C:\Users\Advaith GVK\Downloads\IHR\Merritt_TheMetalMonster.txt"
count_all=Counter()
punctuat= list(string.punctuation)
punctuat.append("--" )
punctuat.append("``" )
stop = stopwords.words('english') + punctuat
stop.append('``')
stop.append("''")
stopterm=["us","'s","like","though","could","upon","within","came","saw","said"]
stop = stop + stopterm 
#print stop
#print data
sent_detector=nltk.data.load('tokenizers/punkt/english.pickle')
ofile=open("out.csv","w")
#ofile1=open("out1.csv","w")
writer=csv.writer(ofile)
writer.writerow(['Sentence','Broken','Class'])
text=nltk.corpus.gutenberg.raw(path)
sentences = sent_detector.tokenize(text.strip())
pattern= r'''\w'''
for sent in sentences:    
    sent=sent.replace('\n',' ')
    tokens=nltk.word_tokenize(sent.lower())
    terms_all=[term for term in tokens if term not in stop]
    added = ' '.join(terms_all)
    print added
    writer.writerow([sent,added," "])
    count_all.update(terms_all)
print(count_all.most_common(15))
ofile.close()

# print(len(brown.words(categories="science_fiction")))

