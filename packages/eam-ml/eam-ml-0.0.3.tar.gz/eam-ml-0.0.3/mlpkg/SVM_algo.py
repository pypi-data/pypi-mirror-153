# # SVM Algorithm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
data1 = load_breast_cancer()

df = pd.DataFrame(data1.data, columns=data1.feature_names)
print(df.head())

y = data1.target

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.3, stratify=y, random_state=42)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
norm = StandardScaler()

mean_area = norm.fit(X_train['mean area'].values.reshape(-1,1))
worst_per = norm.fit(X_train['worst perimeter'].values.reshape(-1,1))
worst_area = norm.fit(X_train['worst area'].values.reshape(-1,1))

X_train['mean area'] = mean_area.transform(X_train['mean area'].values.reshape(-1,1))
X_test['mean area'] = mean_area.transform(X_test['mean area'].values.reshape(-1,1))

X_train['worst perimeter'] = worst_per.transform(X_train['worst perimeter'].values.reshape(-1,1))
X_test['worst perimeter'] = worst_per.transform(X_test['worst perimeter'].values.reshape(-1,1))

X_train['worst area'] = worst_area.transform(X_train['worst area'].values.reshape(-1,1))
X_test['worst area'] = worst_area.transform(X_test['worst area'].values.reshape(-1,1))

from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import RandomizedSearchCV

params = {'C': [0.001, 0.01, 0.1, 1, 10], 'kernel': ['rbf', 'linear', 'poly']}

clf = SVC()

search = RandomizedSearchCV(clf, params, cv=3, return_train_score=True)
search.fit(X_train, y_train)

print(search.best_params_)

# ### Fitting a SVC model with C = 1 and kernel = 'linear'

svm1 = SVC(C=1,kernel='linear')

svm1.fit(X_train, y_train)

y_pred = svm1.predict(X_test)

cf = confusion_matrix(y_test, y_pred)
sns.heatmap(cf, annot=True, cmap="Accent", fmt='g')
plt.show()

from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,y_pred) * 100,"%")

svm1 = SVC(C=1,kernel='rbf')

svm1.fit(X_train, y_train)

y_pred = svm1.predict(X_test)

cf = confusion_matrix(y_test, y_pred)
sns.heatmap(cf, annot=True, cmap="Accent", fmt='g')
plt.show()

from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,y_pred) * 100,"%")

svm1 = SVC(C=1,kernel='poly')

svm1.fit(X_train, y_train)

y_pred = svm1.predict(X_test)

cf = confusion_matrix(y_test, y_pred)
sns.heatmap(cf, annot=True, cmap="Accent", fmt='g')
plt.show()

from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,y_pred) * 100,"%")
