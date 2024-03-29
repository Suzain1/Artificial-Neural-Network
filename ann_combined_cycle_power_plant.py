# -*- coding: utf-8 -*-
"""ANN_Combined_cycle_power_plant.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bDOfwJkLp7SM2fRZxa11QdczTfkNNsOR

#**Importing Necessary Libraries**
"""

import numpy as np
import pandas as pd

"""#**Loading the Combined Cycle Power Plant Dataset**

The dataset contains 9568 data points collected from a Combined Cycle Power Plant over 6 years (2006-2011), when the power plant was set to work with full load. Features consist of **hourly average ambient variables Temperature (AT)**, **Ambient Pressure (AP)**, **Relative Humidity (RH)** and **Exhaust Vacuum (V)** to predict the net **hourly electrical energy output (PE)** of the plant.

* **Dataset link:**
 https://archive.ics.uci.edu/ml/datasets/Combined+Cycle+Power+Plant




"""

Powerplant_data = pd.read_excel('Folds5x2_pp.xlsx')
Powerplant_data.head(5)

"""#**Accessing the Column Names in the Dataset**"""

Powerplant_data.columns

"""#**Finding the Shape of the Dataset**"""

Powerplant_data.shape

Powerplant_data.info()

"""#**Checking Missing Values**"""

Powerplant_data.isna().sum()

"""# **Number of Unique Items in Each Column**"""

Powerplant_data.nunique()

"""#**Seperating Label from Data**"""

X = Powerplant_data.iloc[:, :-1].values
y = Powerplant_data.iloc[:, -1].values

"""or"""

# y = Powerplant_data['PE']
# X = Powerplant_data.drop(['PE'],axis=1)

"""#**Splitting the Data into Training and Testing**"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, shuffle=True)
X_train, X_val, y_train, y_val = train_test_split(X_train,y_train, test_size = 0.2, shuffle=True)

print("Shape of the X_train", X_train.shape)
print("Shape of the X_test", X_test.shape)
print("Shape of the X_val", X_val.shape)
print("Shape of the y_train", y_train.shape)
print("Shape of the y_test", y_test.shape)
print("Shape of the y_val", y_val.shape)

"""#**Building the ANN Model**"""

# sequential model to initialise our ann and dense module to build the layers
from keras.models import Sequential
from keras.layers import Dense

classifier = Sequential()
# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 8, kernel_initializer = 'uniform', activation = 'relu', input_dim = 4))

# Adding the second hidden layer
classifier.add(Dense(units = 16, kernel_initializer = 'uniform', activation = 'relu'))

# Adding the third hidden layer
classifier.add(Dense(units = 32, kernel_initializer = 'uniform', activation = 'relu'))

# Adding the output layer
classifier.add(Dense(units = 1, kernel_initializer = 'uniform'))

"""# **Compiling and Fitting the Model**"""

classifier.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['MeanSquaredLogarithmicError'])

# Fitting the ANN to the Training set
model = classifier.fit(X_train, y_train, batch_size = 32, epochs = 200,validation_data=(X_val, y_val),
              shuffle=True)

"""#**Testing the Model**"""

y_pred = classifier.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

"""#**Metric values**

**MAE (Mean Absolute Error) :-**

$$MAE = (\frac{1}{n})\sum_{i=1}^{n}\left | y_{i} - \hat y_{i} \right |$$

**MSE (Mean Square Error) :-**

$$MSE = (\frac{1}{n})\sum_{i=1}^{n}\left ( y_{i} - \hat y_{i} \right )^2$$

where y = actual value in the data set ;  $\hat y$ = value computed by solving the regression equation

**RMSE (Root Mean Square Error) :-**

$$RMSE = \sqrt{(\frac{1}{n})\sum_{i=1}^{n}\left ( y_{i} - \hat y_{i} \right )^2}$$

"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

import sklearn.metrics
from math import sqrt
mae_no = sklearn.metrics.mean_absolute_error(y_test,classifier.predict(X_test))
mse_no = sklearn.metrics.mean_squared_error(y_test,classifier.predict(X_test))
rms = sqrt(sklearn.metrics.mean_squared_error(y_test,classifier.predict(X_test)))

print('Mean Absolute Error     :',mae_no)
print('Mean Square Error       :',mse_no)
print('Root Mean Square Error:', rms)



