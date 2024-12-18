#!/usr/bin/env python
# coding: utf-8

#import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import linear_model, datasets,metrics
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.utils import to_categorical

# import Iris dataset from Scikit-Learn's datasets
iris = datasets.load_iris()

print ("Shape of the data ", iris.data.shape)
print ("Shape of the data ", iris.target_names)
print ("Attributes ", iris.feature_names)

#view first 5 rows
print (iris.data[range(5)])
print (iris.target[range(5)])

#show it as a table
df = pd.DataFrame(data=iris.data)
df.columns = [iris.feature_names]
df['Class'] = iris.target
df['Name'] = iris.target_names[iris.target]
df.head()

X = iris.data[:, :2]  # we only take the first two features.
Y = iris.target

X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=0)
X_train.shape, y_train.shape
X_test.shape, y_test.shape

# Categorical data must be converted to a numerical form. 

def one_hot_encode_object_array(arr):
    '''One hot encode a numpy array of objects (e.g. strings)'''
    uniques, ids = np.unique(arr, return_inverse=True)
    return to_categorical(ids, len(uniques))

y_train_ohe = one_hot_encode_object_array(y_train)
y_test_ohe= one_hot_encode_object_array(y_test)

# Build Model
model = Sequential()
model.add(Dense(16, input_shape=(4,)))
model.add(Activation('sigmoid'))
model.add(Dense(3))
model.add(Activation('softmax'))
model.summary()

# Optimizer
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["accuracy"])

# Model Training
model.fit(X_train, y_train_ohe, epochs=10, batch_size=5, verbose=1);

# Model Evaluation
loss, accuracy = model.evaluate(X_test, y_test_ohe, verbose=1)
print("Accuracy = {:.2f}".format(accuracy))

classes = np.argmax(model.predict(X_test), axis=-1);

confusion_matrix =  pd.crosstab(index=y_test, columns=classes.ravel(), rownames=['Expected'], colnames=['Predicted'])
print(confusion_matrix)