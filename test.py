import pickle
import numpy as np
import pandas as pd
df = pd.read_csv('train.csv')
dist = df['Location'].unique()
distdict = {}
num = 1
for i in dist:
                distdict[i] = num
                num = num+1
model=pickle.load(open('model.pkl','rb'))
int_features=[int(float(x)) for x in [   6  ,474 ,  24 , 152, 1239 ,   0 ,   1  ,  1  ,  1 ,   5  ,  5 ,  64 ,  20 , 175]]
final = [np.array(list(int_features))]
prediction = model.predict(final)
print(prediction[0])

