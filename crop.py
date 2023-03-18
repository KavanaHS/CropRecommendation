import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import warnings
import pickle
warnings.filterwarnings("ignore")

df = pd.read_csv('train.csv')
dist = df['Location'].unique()
distdict = {}
num = 1
for i in dist:
                distdict[i] = num
                num = num+1
x = df[['Location','rain','Humidity', 'Min Temperature', 'Max Temperature', 'Moisture level', 'Min Ph','Max Ph']]
x = np.array(x)
for i in x:
                i[0] = int(distdict[i[0]])
y = df['Crop']
y = np.array(y)
X_train,X_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 0)
clf = RandomForestClassifier(n_estimators=230,criterion='entropy',max_depth=6,max_features=1,min_samples_leaf=1).fit(X_train,y_train)
pickle.dump(clf,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))
