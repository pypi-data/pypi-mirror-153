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