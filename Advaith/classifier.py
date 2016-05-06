'''
Created on Apr 29, 2016

@author: Advaith GVK
'''
from textblob.classifiers import NaiveBayesClassifier
from sklearn import svm
import openpyxl
from functools import partial
from operator import is_not
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
import csv
from openpyxl import load_workbook
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import SGDClassifier

wb = load_workbook(filename='C:/Users/Advaith GVK/workspace/Trial/src/Pack/result.xlsx', read_only=True)
names=[sheet for sheet in wb.get_sheet_names()]
ws= wb[names[2]]
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

testX=[]
sentX=[]
for i in range(i-1):
    if table[i][1]!= None:
        sentX.append(table[i][0])
        testX.append(table[i][1])
testX=testX[1:]
sentX=sentX[1:] 
df= pd.read_csv("C:/Users/Advaith GVK/workspace/Trial/src/Pack/traindata.csv")
columns_to_keep = [u'Words',u'Label']
df=df[columns_to_keep]
print df
length=len(df)
x=df[u'Words']
y=df[u'Label']
#------------------creating training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.1, random_state=42)
print X_train,Y_train

 
#----------Building classifier 
 
text_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                            alpha=1e-3, n_iter=5, random_state=42)),
 ])
testlab=Y_test
text_clf = text_clf.fit(X_train, Y_train)
predicted = text_clf.predict(X_test)
print len(predicted),len(X_test)
print np.mean(predicted == Y_test)
#writer.writerow(["Label","Predicted Label"  ])
i=1
for label in testlab:
    if(i<len(testlab)):
#       writer.writerow([label,predicted[i]])
        print label,predicted[i]
#-------Classifier metrics
print np.mean(predicted == Y_test)
 
from sklearn import metrics
print(metrics.classification_report(Y_test, predicted))
  
print metrics.confusion_matrix(Y_test, predicted)
 
#-----------Predicting values on database and writing to csv
 
ypredict= text_clf.predict(testX)
result=pd.DataFrame({'Sentence':sentX,'Keywords':testX,'Label':ypredict,'File':names[2]}) 
#result= result.loc[result['Label']=='S']
print len(ypredict),len(testX)
print result
ofile=open("testout.csv","w")
result.to_csv(ofile,cols=['Sentence','Keywords','Label','File'])