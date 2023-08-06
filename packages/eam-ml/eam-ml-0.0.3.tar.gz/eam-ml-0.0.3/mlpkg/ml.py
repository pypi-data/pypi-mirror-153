# %% [markdown]
# From Inbuilt Dataset Technique 1 

# %%
from sklearn import datasets
diabetes = datasets.load_diabetes()
print(diabetes.DESCR)
print(diabetes.feature_names)
X = diabetes.data
Y = diabetes.target
print(X.shape, Y.shape)

# %% [markdown]
# From Inbuilt Dataset Technique 2

# %%
from sklearn import datasets
X, Y = datasets.load_diabetes(return_X_y=True)
print(X.shape, Y.shape)

# %% [markdown]
# From CSV File

# %%
import pandas as pd
#! wget https://github.com/dataprofessor/data/raw/master/BostonHousing.csv
data = pd.read_csv("data.csv")
print(data.head(5))
X = data.drop(['medv'], axis=1)
Y = data.medv
print(X.shape, Y.shape)

X=data.iloc[:,0:2].values
Y=data.iloc[:,-1].values

X=data[['col1','col2']].values
Y=data[['col3']].values

# %% [markdown]
# ScatterPlot Linear or Non Linear

# %%
import seaborn as sns
import matplotlib.pyplot as plt

vals = df_scale.values
plt.scatter(vals[:, 0], vals[:, 1])
plt.show()
# or
plt.scatter(df.age,df.bought_insurance,marker='+',color='red')
plt.show()
# or
ax = sns.scatterplot(data= df_scale, x='Humidity', y='Temperature', s=14)
plt.show()
#or
sns.scatterplot(data['sepal_length'],data['petal_length'],hue=data['species'])

# %% [markdown]
# Imbalance Data

# %%
g = sns.countplot(data['Class'])
g.set_xticklabels(['Not Fraud','Fraud'])
plt.show()

# class count
class_count_0, class_count_1 = data['Class'].value_counts()
# Separate class
class_0 = data[data['Class'] == 0]
class_1 = data[data['Class'] == 1]
# print the shape of the class
print('class 0:', class_0.shape)
print('class 1:', class_1.shape)

# Random Under-Sampling
class_0_under = class_0.sample(class_count_1)
test_under = pd.concat([class_0_under, class_1], axis=0)
print("total class of 1 and 0:",test_under['Class'].value_counts())
# plot the count after under-sampeling
test_under['Class'].value_counts().plot(kind='bar', title='count (target)')

# Random Over-Sampling
class_1_over = class_1.sample(class_count_0, replace=True)
test_over = pd.concat([class_1_over, class_0], axis=0)
print("total class of 1 and 0:",test_under['Class'].value_counts())
# plot the count after under-sampeling
test_over['Class'].value_counts().plot(kind='bar', title='count (target)')

# %%
data['species']=data['species'].replace({'setosa':1,'versicolor':0})

# %% [markdown]
# Train and Test Data Split

# %%
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
print(X_train.shape)
print(Y_train.shape)

# %% [markdown]
# Linear Regression

# %%
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
model = linear_model.LinearRegression()
model.fit(X_train[:,:1], Y_train)
Y_pred = model.predict(X_test[:,:1])
print('Coefficients:', model.coef_)
print('Intercept:', model.intercept_)
print('Mean squared error (MSE): %.2f' % mean_squared_error(Y_test, Y_pred))
print('Coefficient of determination (R^2): %.2f' % r2_score(Y_test, Y_pred))

# %% [markdown]
# Multi Linear Regression

# %%
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
model = linear_model.LinearRegression()
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test[:,:1])
print('Coefficients:', model.coef_)
print('Intercept:', model.intercept_)
print('Mean squared error (MSE): %.2f' % mean_squared_error(Y_test, Y_pred))
print('Coefficient of determination (R^2): %.2f' % r2_score(Y_test, Y_pred))

# %% [markdown]
# Logistic Regression

# %%
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)
Y_pred_prob = model.predict_proba(X_test)
print('Coefficients:', model.coef_)
print('Intercept:', model.intercept_)
print('Accuracy Score: %.2f' % model.score(X_test,Y_test))

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
print(classification_report(Y_test, Y_pred))
print(confusion_matrix(Y_test, Y_pred))
print(accuracy_score(Y_test, Y_pred))

import seaborn as sns
import matplotlib.pyplot as plt
sns.heatmap(pd.DataFrame(confusion_matrix(Y_test, Y_pred)))
plt.show()

# %% [markdown]
# Perceptron

# %%
from sklearn.linear_model import Perceptron
clf=Perceptron()
clf.fit(X_train,Y_train)
Y_pred=clf.predict(X_test)
#clf.plot()

from sklearn.metrics import accuracy_score
print(accuracy_score(Y_test,Y_pred))
print(clf.coef_)
print(clf.intercept_)

from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X, y, clf=clf, legend=2)
# or
sns.scatterplot(data['marks1'],data['marks2'],hue=data['result'])

# %% [markdown]
# MLP

# %%
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(max_iter=500, activation='relu')
print(mlp)
pred = mlp.predict(X_test)
print(pred)
from sklearn.metrics import classification_report,confusion_matrix
print(confusion_matrix(Y_test,pred))
print(classification_report(Y_test,pred))

# %% [markdown]
# SVM

# %%
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV

params = {'C': [0.001, 0.01, 0.1, 1, 10], 'kernel': ['rbf', 'linear', 'poly']}
clf = SVC()
search = RandomizedSearchCV(clf, params, cv=3, return_train_score=True)
search.fit(X_train, Y_train)
print(search.best_params_)
print(search.best_score_)

# ### Fitting a SVC model with C = 1 and kernel = 'linear'
svm1 = SVC(C=1,kernel='linear')
svm1.fit(X_train, Y_train)
y_pred = svm1.predict(X_test)
cf = confusion_matrix(Y_test, y_pred)
sns.heatmap(cf, annot=True, cmap="Accent", fmt='g')
plt.show()
print(accuracy_score(Y_test,y_pred) * 100,"%")

svm1 = SVC(C=1,kernel='rbf')
svm1.fit(X_train, Y_train)
y_pred = svm1.predict(X_test)
cf = confusion_matrix(Y_test, y_pred)
sns.heatmap(cf, annot=True, cmap="Accent", fmt='g')
plt.show()
print(accuracy_score(Y_test,y_pred) * 100,"%")

svm1 = SVC(C=1,kernel='poly')
svm1.fit(X_train, Y_train)
y_pred = svm1.predict(X_test)
cf = confusion_matrix(Y_test, y_pred)
sns.heatmap(cf, annot=True, cmap="Accent", fmt='g')
plt.show()
print(accuracy_score(Y_test, y_pred) * 100,"%")

# %% [markdown]
# Decision Tree 

# %%
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=4)
clf = clf.fit(X_train, Y_train)
print(clf.get_params())
print(clf.predict_proba(X_test))
Y_pred = clf.predict(X_test)
print(Y_pred)
from sklearn.metrics import precision_score,confusion_matrix,accuracy_score, classification_report
print(confusion_matrix(Y_test, Y_pred, label=[0,1]))
print(accuracy_score(Y_test, Y_pred))
print(precision_score(Y_test, Y_pred))
print(classification_report(Y_test,pred))

print(clf.feature_importances_)
forest_importances = pd.Series(clf.feature_importances_, index=X.columns)
std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=std, ax=ax)
ax.set_title("Feature importance")
ax.set_ylabel("Feature importance")
fig.tight_layout()
# or
feature_imp = pd.Series(clf.feature_importances_, index = X.columns).sort_values(ascending = False)
print(feature_imp)
data={'feature_names':np.array(X.columns),'feature_importance':np.array(clf.feature_importances_)}
dfi = pd.DataFrame(data)
dfi.sort_values(by=['feature_importance'], ascending=False,inplace=True)
plt.figure(figsize=(14,7))
sns.barplot(x=dfi['feature_importance'], y=dfi['feature_names'])
plt.title('FEATURE IMPORTANCE')
plt.xlabel('FEATURE IMPORTANCE')
plt.ylabel('FEATURE NAMES')
plt.show()

from sklearn.tree import plot_tree
fig = plt.figure(figsize=(25,20))
_ = plot_tree(clf,feature_names=X.columns,class_names={0:"Malignant",1:"Benign"},filled=True,fontsize=12)

# %% [markdown]
# Random Forest

# %%
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import OrderedDict

def display_feature_importance(importance,feature_names,model_type):
    print(F"FEATURE IMPORTANCE {model_type}: ")
    feature_imp = pd.Series(importance, index = feature_names).sort_values(ascending = False)
    print(feature_imp)

    data={'feature_names':np.array(feature_names),'feature_importance':np.array(importance)}
    fi_df = pd.DataFrame(data)
    fi_df.sort_values(by=['feature_importance'], ascending=False,inplace=True)

    plt.figure(figsize=(14,7))
    sns.barplot(x=fi_df['feature_importance'], y=fi_df['feature_names'])
    plt.title(model_type + ' FEATURE IMPORTANCE')
    plt.xlabel('FEATURE IMPORTANCE')
    plt.ylabel('FEATURE NAMES')
    plt.show()

# RandomForestClassifier
clf = RandomForestClassifier(n_estimators = 100)
clf.fit(X_train, Y_train)
print("MEAN ABSOLUTE ERROR OF RANDOM FOREST CLASSIFIER : ",mean_absolute_error(Y_test, clf.predict(X_test)))
print("ACCURACY OF THE RANDOM FOREST CLASSIFIER : ",clf.score(X_test, Y_test))
# result = clf.predict([[3, 3, 2, 2]])
display_feature_importance(clf.feature_importances_,iris.feature_names,'RANDOM FOREST CLASSIFIER')

# RandomForestRegressor
rf_mae = RandomForestRegressor(oob_score=True, criterion='absolute_error',
                                n_estimators=400, max_features=0.4, max_depth=20, n_jobs=-1)
rf_mae.fit(X_train, Y_train)
print("MEAN ABSOLUTE ERROR OF RANDOM FOREST REGRESSOR : ",mean_absolute_error(Y_test, rf_mae.predict(X_test)))
print("ACCURACY OF THE RANDOM FOREST REGRESSOR : ",rf_mae.score(X_test, Y_test))
display_feature_importance(rf_mae.feature_importances_,iris.feature_names,'RANDOM FOREST REGRESSOR')

# GridSearchCV
param_dict = OrderedDict(
    n_estimators = [200,400,600,800],
    max_features = [0.2, 0.4, 0.6, 0.8],
    max_depth=[5,10,15,20]
)
est2 = RandomForestRegressor(oob_score=False, criterion='absolute_error')
gs = GridSearchCV(est2, param_grid = param_dict, cv=5, n_jobs=-1)
gs.fit(X_train, Y_train)
print("BEST ESTIMATOR CONFIG : ")
rf2 = gs.best_estimator_
print(rf2)
print("BEST ESTIMATOR ACCURACY : ")
print(gs.best_score_)
rf2.fit(X_train, Y_train)
print("MEAN ABSOLUTE ERROR OF RANDOM FOREST REGRESSOR : ",mean_absolute_error(Y_test, rf2.predict(X_test)))
print("ACCURACY OF THE RANDOM FOREST REGRESSOR : ", rf2.score(X_test, Y_test))

# %% [markdown]
# Adaboost

# %%
import sklearn.metrics as metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

depth = [1,2,3,4,5]
iteration = range(1,100,5)

accuracies_train = []
accuracies_test = []
# trees = [2**x for x in range(8)]
for md in depth:
    depth_accuracies_train = []
    depth_accuracies_test = []
    for n in iteration:
        ada=AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=md),n_estimators=n, learning_rate=0.05)
        depth_accuracies_train.append(metrics.accuracy_score(Y_train, ada.fit(X_train,Y_train).predict(X_train)))
        depth_accuracies_test.append(metrics.accuracy_score(Y_test, ada.fit(X_train,Y_train).predict(X_test)))
    accuracies_train.append(depth_accuracies_train)
    accuracies_test.append(depth_accuracies_test)

for i, md in enumerate(depth):
    plt.semilogx(iteration, accuracies_train[i], label='Max Depth {}'.format(md))
plt.legend(loc=4)
plt.title('Iteration vs Accuracy due to depth')
plt.xlabel('Iteration')
plt.ylabel('Accuracy')
plt.show()

training_error = []
test_error = []
for i in iteration:    
    adaboost = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=i, learning_rate=0.05)
    adaboost.fit(X_train, Y_train)
    training_error.append(1-adaboost.score(X_train, Y_train))
    test_error.append(1-adaboost.score(X_test, Y_test))

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.plot(iteration, training_error, color='red', alpha=0.8, label='training error')
ax.plot(iteration, test_error, color='blue', alpha=0.8, label='test error')
ax.set_title('Comparison of Errors')
ax.set_xlabel('Iterations')
ax.legend(loc='best')
plt.show()

# %% [markdown]
# Stacking

# %%
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier
from sklearn.model_selection import cross_val_score
import xgboost
import pandas as pd

df = datasets.load_breast_cancer()
X = pd.DataFrame(columns = df.feature_names, data = df.data)
print("Dataset : \n",X.head(5))
y = df.target

dtc =  DecisionTreeClassifier()
rfc = RandomForestClassifier()
knn =  KNeighborsClassifier()
xgb = xgboost.XGBClassifier()

# Individual Classifier
clf = [('Decision Tree',dtc),('Random Forest',rfc),('K Neighbors',knn),('XG Boost',xgb)]
for name,model in clf:
    score = cross_val_score(model,X,y,cv = 5,scoring = 'accuracy')
    print(f"The accuracy score of {name} is : ",score.mean())

lr = LogisticRegression()

# Stacking Classifier
stack_model = StackingClassifier( estimators = clf, final_estimator = lr)
score = cross_val_score(stack_model,X,y,cv = 5,scoring = 'accuracy')
print("The accuracy score of stacking is : ",score.mean())

# Voting Classifier with hard voting
vot_hard = VotingClassifier(estimators = clf, voting ='hard')
score = cross_val_score(vot_hard,X,y,cv = 5,scoring = 'accuracy')
print("Hard Voting Score : ",score.mean())

# Voting Classifier with soft voting
vot_soft = VotingClassifier(estimators = clf, voting ='soft')
score = cross_val_score(vot_hard,X,y,cv = 5,scoring = 'accuracy')
print("Soft Voting Score : ",score.mean())

# %% [markdown]
# K means

# %%
from sklearn.cluster import KMeans
from kneed import KneeLocator
from sklearn.metrics import silhouette_score

K=range(2,12)
wcss = [] 
for k in K:
    kmeans = KMeans(n_clusters = k, init = 'k-means++', random_state = 42) 
    kmeans.fit(df) 
    wcss.append(kmeans.inertia_)

plt.plot(K, wcss) 
plt.xlabel('Number of clusters (K)') 
plt.ylabel('Within-Cluster-Sum of Squared Errors (WSS)') 
plt.show() 

kl = KneeLocator(K, wcss, curve="convex", direction="decreasing")
k_wcss = kl.elbow
print("Optimal K value by WCSS Elbow Method : ", k_wcss)

# 2) The Silhouette Method
silhouette = []
for k in K:
    kmeans = KMeans(n_clusters = k, init = 'k-means++', random_state = 42) 
    kmeans.fit(df) 
    silhouette.append(silhouette_score(df,kmeans.labels_,metric="euclidean",sample_size=1000,random_state=200))

plt.plot(K, silhouette) 
plt.xlabel('Number of clusters (K)') 
plt.ylabel('Silhouette Score') 
plt.show() 

k_silh = silhouette.index(max(silhouette)) + 2
print("Optimal K value by The Silhouette Method : ",k_silh) 

k_opt = k_wcss
kmeans = KMeans(n_clusters = k_opt, init = 'k-means++', random_state = 42) 
y_kmeans = kmeans.fit_predict(df)

df['Clusters'] = kmeans.labels_
ax = sns.scatterplot(data= df, x='websites purchased so far', y='hours spend per week', hue = 'Clusters', palette='viridis', alpha=0.75, s=12)
ax = sns.scatterplot(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], hue=range(k_opt), palette='viridis', s=25, ec='black', legend=False, ax=ax)
plt.show() 

score = metrics.accuracy_score(y_test,k_means.predict(X_test))

# %% [markdown]
# SOM R Studio

# %%
install.packages("kohonen")
library(kohonen)
data <- read.csv("data.csv", header = T)
str(data)
set.seed(222)
X <- scale(data[,-1])
summary(X)
g <- somgrid(xdim = 4, ydim = 4, topo = "rectangular" )
map <- som(X,
           grid = g,
           alpha = c(0.05, 0.01),
           radius = 1)
plot(map, type='codes',palette.name = rainbow)
map$unit.classif
map$codes

plot(map, type = "mapping")

//supervised som

set.seed(123)
ind <- sample(2, nrow(data), replace = T, prob = c(0.7, 0.3))
train <- data[ind == 1,]
test <- data[ind == 2,]

//normalisation
trainX <- scale(train[,-1])
testX <- scale(test[,-1],
               center = attr(trainX, "scaled:center"),
               scale = attr(trainX, "scaled:scale"))
trainY <- factor(train[,1])
Y <- factor(test[,1])
test[,1] <- 0
testXY <- list(independent = testX, dependent = test[,1])

//gradient boosting 
set.seed(223)
map1 <- xyf(trainX,
            classvec2classmat(factor(trainY)),
            grid = somgrid(5, 5, "hexagonal"),
            rlen = 100)
plot(map1, type='codes',palette.name = rainbow)

//cluster boundary 
par(mfrow = c(1,2))
plot(map1,
     type = 'codes',
     main = c("Codes X", "Codes Y"))
map1.hc <- cutree(hclust(dist(map1$codes[[2]])), 2)
add.cluster.boundaries(map1, map1.hc)
par(mfrow = c(1,1))

//prediction
pred <- predict(map1, newdata = testXY)
table(Predicted = pred$predictions[[2]], Actual = Y)

# %% [markdown]
# Find S
# Outlook,Temperature,Humidity,Wind,PlayTennis
# Overcast,Hot,High,Weak,Yes
# Rain,Mild,High,Weak,Yes
# Rain,Cool,Normal,Strong,No
# Overcast,Cool,Normal,Weak,Yes

# %%
import pandas as pd
import numpy as np

print("\n FIND S ALGORITHM : ELAVAZHAKAN A = 21MAI0048")

data = pd.read_csv(".\ML LAB\Lab 1\data_fs.csv")
print(data,'\n')

attr = np.array(data)[:,:-1]
print("\n The attributes are: ",attr)

target = np.array(data)[:,-1]
print("\n The target is: ",target)

def train(a,t):
    for i, val in enumerate(t):
        if val == "Yes":
            specific_hypothesis = a[i].copy()
            break
    
    print("\n The chosen specific_hypothesis is: ",specific_hypothesis)

    for i, val in enumerate(a):
        if t[i] == "Yes":
            for x in range(len(specific_hypothesis)):
                if val[x] != specific_hypothesis[x]:
                    specific_hypothesis[x] = '?'
                else:
                    pass
        print("\n Hypothesis Step no ",i," is: ",specific_hypothesis)    
    
    return specific_hypothesis

print("\n The final hypothesis is:",train(attr,target))

# %% [markdown]
# Candidate Elimination
# sky,airtemp,humidity,wind,water,forcast,enjoysport
# sunny,warm,normal,strong,warm,same,yes
# sunny,warm,high,strong,warm,same,yes
# rainy,cold,high,strong,warm,change,no
# sunny,warm,high,strong,cool,change,yes

# %%
import numpy as np 
import pandas as pd

data = pd.read_csv('.\ML LAB\Lab 1\data_ce.csv')
concepts = np.array(data.iloc[:,0:-1])
print("\nInstances are:\n",concepts)
target = np.array(data.iloc[:,-1])
print("\nTarget Values are: ",target)

def learn(concepts, target): 
    print("\nInitialization of specific_h and genearal_h")
    specific_h = concepts[0].copy()
    print("\nSpecific Boundary: ", specific_h)
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    print("\nGeneric Boundary: ",general_h)  

    for i, h in enumerate(concepts):
        print("\nInstance", i+1 , "is ", h)
        if target[i] == "yes":
            print("Instance is Positive ")
            for x in range(len(specific_h)): 
                if h[x]!= specific_h[x]:                    
                    specific_h[x] ='?'                     
                    general_h[x][x] ='?'
                   
        if target[i] == "no":            
            print("Instance is Negative ")
            for x in range(len(specific_h)): 
                if h[x]!= specific_h[x]:                    
                    general_h[x][x] = specific_h[x]                
                else:                    
                    general_h[x][x] = '?'        
        
        print("Specific Bundary after ", i+1, "Instance is ", specific_h)         
        print("Generic Boundary after ", i+1, "Instance is ", general_h)
        print("\n")

    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]    
    for i in indices:   
        general_h.remove(['?', '?', '?', '?', '?', '?']) 
    return specific_h, general_h 

s_final, g_final = learn(concepts, target)

print("Final Specific_h: ", s_final, sep="\n")
print("Final General_h: ", g_final, sep="\n")

# %% [markdown]
# PCA 

# %%
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X1 = pca.fit_transform(X)
X1.shape

# %% [markdown]
# FactorAnalysis

# %%
from sklearn.decomposition import FactorAnalysis
fa = FactorAnalysis(n_components=2)
X_ = fa.fit_transform(X)


