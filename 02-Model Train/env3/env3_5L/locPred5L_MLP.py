# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 04:39:20 2024

@author: emree
"""

# prepare data for lstm
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Flatten
from sklearn.model_selection import train_test_split
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)



def normalize(table,column,outMin,outMax,hMinMax,hMin,hMax):
    # outMin=0.1
    # outMax=1
    table_scaled = table.copy()
    x=table_scaled[column]
    
    if(hMinMax==True):
        inMin=hMin
        inMax=hMax
    else:    
        inMin=table_scaled [column].min()
        inMax=table_scaled[column].max()
    
    minVal=inMin
    maxVal=inMax

    table_scaled[column]=(x-inMin)*(outMax-outMin)/(inMax-inMin)+outMin
  
    return table_scaled,maxVal,minVal 

normList=[]

# load dataset

datasetName="dataSet_5L"

dataset= read_csv(datasetName+".csv", header=0)

# Normalize Data Set
header_list = list(dataset.columns)
for i in range(0, len(header_list)):
    dataset,aMax,bMin=normalize(dataset,header_list[i],0,1,False,0,0)
    normList.append([header_list[i],bMin,aMax])
    
# NormList Save
with open(datasetName+'normList.txt', 'w') as file:
    file.write('[')
    for i in range(0, len(normList)-1):
        # print(item)
        file.write(str(normList[i])+ ',') 
    file.write(str(normList[len(normList)-1]))     
    file.write(']')


dataNum=len(dataset.columns)


# %% split into input (X) and output (Y) variables
values = dataset.values
values = values.astype('float32')

X = values[:,0:dataNum-2]
Y = values[:,dataNum-2:dataNum]

inputNum=X.shape[1]
outNum=Y.shape[1]



# %% Model Architecture

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.05, random_state=1)

model = Sequential()
model.add(Dense(inputNum, input_shape=(inputNum,), kernel_initializer='normal', activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Dense(1024, activation='relu'))
model.add(Dense(1024, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(outNum))
model.summary()

optimizer = optimizers.Adam(lr=0.0001)
# optimizer = optimizers.Adam(lr=0.000001)
model.compile(loss='mse', optimizer=optimizer, metrics=['accuracy','mse', 'mae', 'mape'])
batch_size_val = 1024

# %% Model Train

# simple early stopping
from keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='loss', patience=10, verbose=1)

# fit model
# history=model.fit(X_train, y_train, validation_split=0.2, batch_size=batch_size_val, epochs=1000, verbose=1)
history=model.fit(X_train, y_train, validation_split=0.2, batch_size=batch_size_val, epochs=1000, verbose=1, callbacks=[es])

# %% Model Plot
def draw(xL,yL,ax,p,cVal,vVal,ok):
    ax.annotate(str(round(yL[p],4)),fontsize=14,
                xy=(xL[p], yL[p]), xycoords='data',color=cVal,
                xytext=(-90, vVal), textcoords='offset points',
                bbox=dict(boxstyle="round", fc='white'),
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB="+ok+",rad=10",color=cVal))


from matplotlib import pyplot as plt

plt.figure(figsize=(12,5)) 
F = plt.gcf()
DPI = F.get_dpi()
print(DPI)

print(history.history.keys())
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'],linestyle='--')
plt.xlabel('Epoch', fontsize=16)
plt.ylabel('Total Loss', fontsize=16)

plt.grid(True) 

print("___________________")
print(es.stopped_epoch)


plt.legend(['5L-Train', '5L-Val'],bbox_to_anchor=(0, 1.02, 1, 0.5), loc="lower right", borderaxespad=0, ncol=8,fontsize=12)
# plt.legend(['train', 'val'], loc='upper left')


# Epoch sayısı
epochs = range(1, len(history.history['loss']) + 1)

draw(epochs,history.history['loss'],plt,len(history.history['loss'])-2,'#1f77b4',30,"110")
draw(epochs,history.history['val_loss'],plt,len(history.history['val_loss'])-2,'#ff7f0e',60,"90")


plt.show()

F.tight_layout()

F.savefig(datasetName+"Loss.png", dpi = (200))

preds = model.predict(X_test)

# %% History kaydet
import pandas as pd

# History verisini DataFrame'e çevir
df_history = pd.DataFrame(history.history)

# CSV olarak kaydet
df_history["epoch"] = df_history.index + 1
df_history.to_csv(datasetName+"_Hist.csv", index=False)

print("Kayıt tamamlandı: training_history.csv")

# %% Model Performance

#importing module
import sklearn
# Importing the required module
from sklearn.metrics import r2_score, accuracy_score,mean_squared_error, mean_absolute_error
# Evaluating the model
print('R2 score is :', round(r2_score(y_test, preds),5))
print('Mean Squared Error :',round(mean_squared_error(y_test, preds,squared=True),5))
print('Root Mean Squared Error :',round(mean_squared_error(y_test, preds,squared=False),5))
print('Mean Absolute Error :',round(mean_absolute_error(y_test, preds),5))


# %% Save Model

from tensorflow.keras.models import save_model
save_model(model, "model_"+datasetName+".h5")

