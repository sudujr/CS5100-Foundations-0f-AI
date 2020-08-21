#!/usr/bin/env python
# coding: utf-8

# In[148]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[149]:


columns = ['sl','sw','pl','pw','class']
df = pd.read_csv("iris.data", names= columns)


# In[150]:


df.head()


# In[ ]:





# In[151]:


X = df.drop('class', axis=1)
y = df['class']


# In[157]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)


# In[158]:


from sklearn.svm import LinearSVC

model = LinearSVC()
model.fit(X_train, y_train.ravel())


#Calculate Test Prediction
y_pred = model.predict(X_test)
print(model.score(X_test,y_test.ravel()))

#Plot Confusion Matrix
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

import matplotlib.pyplot as plt
import seaborn as sn

df_cm = pd.DataFrame(cm, index = [i for i in np.unique(y)],
                  columns = [i for i in np.unique(y)])
plt.figure(figsize = (5,5))
sn.heatmap(df_cm, annot=True)
from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test,y_pred))


# In[ ]:




