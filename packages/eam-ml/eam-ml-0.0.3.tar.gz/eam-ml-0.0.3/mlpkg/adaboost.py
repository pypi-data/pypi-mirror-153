import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
import sklearn.metrics as metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split

iris = datasets.load_iris()
print("FEATURE NAMES : \n",iris.feature_names)
print("TARGET NAMES : \n",iris.target_names)

data = pd.DataFrame({'sepallength': iris.data[:, 0], 'sepalwidth': iris.data[:, 1],
                     'petallength': iris.data[:, 2], 'petalwidth': iris.data[:, 3],
                     'species': iris.target})
print("DATASET : \n",data.head())

X, y = datasets.load_iris( return_X_y = True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.10)

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
        depth_accuracies_train.append(metrics.accuracy_score(y_train, ada.fit(X_train,y_train).predict(X_train)))
        depth_accuracies_test.append(metrics.accuracy_score(y_test, ada.fit(X_train,y_train).predict(X_test)))
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
    adaboost.fit(X_train, y_train)
    training_error.append(1-adaboost.score(X_train, y_train))
    test_error.append(1-adaboost.score(X_test, y_test))

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.plot(iteration, training_error, color='red', alpha=0.8, label='training error')
ax.plot(iteration, test_error, color='blue', alpha=0.8, label='test error')
ax.set_title('Comparison of Errors')
ax.set_xlabel('Iterations')
ax.legend(loc='best')
plt.show()
