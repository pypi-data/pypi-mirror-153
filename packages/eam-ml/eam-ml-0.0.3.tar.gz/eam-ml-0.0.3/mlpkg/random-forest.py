from sklearn import datasets
from sklearn.model_selection import train_test_split
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

iris = datasets.load_iris()
print("FEATURE NAMES : \n",iris.feature_names)
print("TARGET NAMES : \n",iris.target_names)

data = pd.DataFrame({'sepallength': iris.data[:, 0], 'sepalwidth': iris.data[:, 1],
                     'petallength': iris.data[:, 2], 'petalwidth': iris.data[:, 3],
                     'species': iris.target})
print("DATASET : \n", data.head())

X, y = datasets.load_iris( return_X_y = True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20,random_state=100)


clf = RandomForestClassifier(n_estimators = 100)
clf.fit(X_train, y_train)

print("MEAN ABSOLUTE ERROR OF RANDOM FOREST CLASSIFIER : ",mean_absolute_error(y_test, clf.predict(X_test)))
print("ACCURACY OF THE RANDOM FOREST CLASSIFIER : ",clf.score(X_test, y_test))

# result = clf.predict([[3, 3, 2, 2]])

display_feature_importance(clf.feature_importances_,iris.feature_names,'RANDOM FOREST CLASSIFIER')

rf_mae = RandomForestRegressor(oob_score=True, criterion='absolute_error',
                                n_estimators=400, max_features=0.4, max_depth=20, n_jobs=-1)
rf_mae.fit(X_train, y_train)

print("MEAN ABSOLUTE ERROR OF RANDOM FOREST REGRESSOR : ",mean_absolute_error(y_test, rf_mae.predict(X_test)))
print("ACCURACY OF THE RANDOM FOREST REGRESSOR : ",rf_mae.score(X_test, y_test))

display_feature_importance(rf_mae.feature_importances_,iris.feature_names,'RANDOM FOREST REGRESSOR')

param_dict = OrderedDict(
    n_estimators = [200,400,600,800],
    max_features = [0.2, 0.4, 0.6, 0.8],
    max_depth=[5,10,15,20]
)


est2 = RandomForestRegressor(oob_score=False, criterion='absolute_error')
gs = GridSearchCV(est2, param_grid = param_dict, cv=5, n_jobs=-1)
gs.fit(X_train, y_train)

print("BEST ESTIMATOR CONFIG : ")
rf2 = gs.best_estimator_
print(rf2)
print("BEST ESTIMATOR ACCURACY : ")
print(gs.best_score_)

rf2.fit(X_train, y_train)

print("MEAN ABSOLUTE ERROR OF RANDOM FOREST REGRESSOR : ",mean_absolute_error(y_test, rf2.predict(X_test)))
print("ACCURACY OF THE RANDOM FOREST REGRESSOR : ", rf2.score(X_test, y_test))