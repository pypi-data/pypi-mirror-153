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