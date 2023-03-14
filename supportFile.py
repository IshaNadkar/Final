#Step1: Importing Required Packages
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import pickle

data_set = pd.read_csv('dataset.csv')
#Step3: Extracting the Predictors and target
predictors = ['l','r','temp','bph','bpl','hr']
target = ['stress']
x = data_set[predictors].values
y = data_set[target].values

print(x)
print(y)

#Step5: Splitting of the Dataset
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=0)

#Step6: Fitting the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion='entropy')
classifier.fit(x_train,y_train)
DTCpred = classifier.predict(x_train)
# save the model to disk
filename = 'DTC.sav'
pickle.dump(classifier, open(filename, 'wb'))

#---------------Accuracy----------------------------
from sklearn import metrics
DTC_accuracy = metrics.accuracy_score(y_train, DTCpred)
print(DTCpred)
print('Accuracy =',DTC_accuracy*100,'%')

def predictStress(testData):
    loaded_model = pickle.load(open('DTC.sav', 'rb'))
    DTC_r = loaded_model.predict(testData)
    print(DTC_r)
    if(DTC_r[0]==0):
        stress = 'Mild/No Stress'
        feedback = '''1.Take breaks from watching, reading, or listening to news stories, including those on social media. ...
                    2.Take care of yourself.
                    3.Take care of your body.
                    4.Make time to unwind.
                    5.Talk to others.
                    6.Connect with your community- or faith-based organizations.
                    7.Avoid drugs and alcohol.
                    '''
    elif(DTC_r[0]==1):
        stress = 'Moderate Stress'
        feedback = '''1.Exercise.
                    2.Relax Your Muscles.
                    3.Deep Breathing.
                    4.Eat Well.
                    5.Slow Down.
                    6.Take a Break.
                    7.Make Time for Hobbies.
                    8.Talk About Your Problems.'''
    elif(DTC_r[0]==2):
        stress = 'Severe Stress'
        feedback = '''1.Take breaks from watching, reading, or listening to news stories, including those on social media. ...
                    2.Take care of yourself. ...
                    3.Take care of your body. ...
                    4.Make time to unwind. ...
                    5.Talk to others. ...
                    6.Connect with your community- or faith-based organizations.
                    7.Avoid drugs and alcohol.'''
    return(stress,feedback)


def timeDiff(tstamp1,tstamp2):
    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))

    print('The difference is approx. %s minutes' % td_mins)
    return td_mins