#!/usr/bin/env python
# coding: utf-8

# In[157]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[181]:


columns = ['class','cap-shape','cap-surface','cap-color','bruises?','odor', 'gill-attachment','gill-spacing','gill-size',
           'gill-color','stalk-shape','stalk-root','stalk-surface-above-ring','stalk-surface-below-ring',
           'stalk-color-above-ring','stalk-color-below-ring','veil-type','veil-color','ring-number','ring-type',
           'spore-print-color','population','habitat']
df = pd.read_csv("agaricus-lepiota.data", names= columns , na_values = "?" )


# In[182]:


df.isnull().values.any()


# In[183]:


df.isnull().sum().sum()


# In[184]:


df['stalk-root'].isnull().sum()


# In[185]:


for column in df.columns:
    df[column].fillna(df[column].mode()[0], inplace=True)


# In[186]:


df.isnull().sum().sum()


# In[187]:


df['stalk-root'].isnull().sum()


# In[188]:


#df.info()
len(df)


# In[189]:


df.head()


# In[190]:


for column in df.columns:
    print(column)


# In[195]:


df.head()


# In[197]:


X = df.drop('class', axis=1)
y = df['class']
from sklearn.preprocessing import LabelEncoder

label_encoder = preprocessing.LabelEncoder()
X = X.apply(LabelEncoder().fit_transform)
print(X.head())


# In[234]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)


# In[235]:


from sklearn.svm import SVC
svm = SVC(random_state = 42)
svm.fit(X_train,y_train)
print("Test Accuracy: {}%".format(round(svm.score(X_test,y_test)*100,2)))


from sklearn.metrics import confusion_matrix
y_pred_lr = svm.predict(X_test)
y_true_lr = y_test
cm = confusion_matrix(y_true_lr, y_pred_lr)
f, ax = plt.subplots(figsize =(5,5))
sns.heatmap(cm,annot = True,linewidths=0.5,linecolor="red",fmt = ".0f",ax=ax)
plt.xlabel("y_pred_lr")
plt.ylabel("y_true_lr")
plt.show()
from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test,y_pred))


# In[ ]:





# In[ ]:




