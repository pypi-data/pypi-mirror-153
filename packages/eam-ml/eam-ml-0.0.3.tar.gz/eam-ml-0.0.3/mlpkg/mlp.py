import numpy as np 
np.random.seed(10)
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
data = pd.read_csv('train.csv')
print(data.head(4))
dict_live = { 
 0 : 'Perished',
 1 : 'Survived'
}
dict_sex = {
 'male' : 0,
 'female' : 1
}
data['Bsex'] = data['Sex'].apply(lambda x : dict_sex[x])
features = data[['Pclass', 'Bsex']].to_numpy()
labels = data['Survived'].to_numpy()
def sigmoid_act(x, der=False):
 import numpy as np
 
 if (der==True) : #derivative of the sigmoid
 f = x/(1-x)
 else : # sigmoid
 f = 1/(1+ np.exp(-x))
 
 return f
def ReLU_act(x, der=False):
 import numpy as np
 
 if (der== True):
 if x>0 :
 f= 1
 else :
 f = 0
 else :
 if x>0:
 f = x
 else :
 f = 0
 return f
def perceptron(X, act='Sigmoid'): 
 import numpy as np
 
 shapes = X.shape 
 n= shapes[0]+shapes[1]
 w = 2*np.random.random(shapes) - 0.5 
 b = np.random.random(1)
 f = b[0]
 for i in range(0, X.shape[0]-1) :
 for j in range(0, X.shape[1]-1) : 
 f += w[i, j]*X[i,j]/n
 if act == 'Sigmoid':
 output = sigmoid_act(f)
 else :
 output = ReLU_act(f)
 
 return output
 
print('Output with sigmoid activator: ', perceptron(features))
print('Output with ReLU activator: ', perceptron(features))
def sigmoid_act(x, der=False):
 import numpy as np
 
 if (der==True) : 
 f = 1/(1+ np.exp(- x))*(1-1/(1+ np.exp(- x)))
 else : 
 f = 1/(1+ np.exp(- x))
 
 return f
def ReLU_act(x, der=False):
 import numpy as np
 
 if (der == True): 
 f = np.heaviside(x, 1)
 else :
 f = np.maximum(x, 0)
 
 return f
X_train, X_test, Y_train, Y_test = train_test_split(features, labels, test_size=0.30)
print('Training records:',Y_train.size)
print('Test records:',Y_test.size)
p=4 
q=4 
eta = 1/623
w1 = 2*np.random.rand(p , X_train.shape[1]) - 0.5
b1 = np.random.rand(p)
w2 = 2*np.random.rand(q , p) - 0.5 
b2 = np.random.rand(q)
wOut = 2*np.random.rand(q) - 0.5 
bOut = np.random.rand(1)
mu = []
vec_y = []
for I in range(0, X_train.shape[0]): 
 x = X_train[I]
 
 z1 = ReLU_act(np.dot(w1, x) + b1) 
 z2 = ReLU_act(np.dot(w2, z1) + b2)
 y = sigmoid_act(np.dot(wOut, z2) + bOut) 
 
 delta_Out = (y-Y_train[I]) * sigmoid_act(y, der=True)
 
 #2.3: Backpropagate
 delta_2 = delta_Out * wOut * ReLU_act(z2, der=True) 
 delta_1 = np.dot(delta_2, w2) * ReLU_act(z1, der=True) 
 
 # 3: Gradient descent 
 wOut = wOut - eta*delta_Out*z2 
 bOut = bOut - eta*delta_Out
 
 w2 = w2 - eta*np.kron(delta_2, z1).reshape(q,p)
 b2 = b2 - eta*delta_2
 
 w1 = w1 - eta*np.kron(delta_1, x).reshape(p, x.shape[0])
 b1 = b1 - eta*delta_1
 
 # 4. Computation of the loss function
 mu.append((1/2)*(y-Y_train[I])**2)
 vec_y.append(y[0])
# Plotting the Cost function for each training data 
plt.figure(figsize=(10,6))
plt.scatter(np.arange(0, X_train.shape[0]), mu, alpha=0.3, s=4, label='mu')
plt.title('Loss for each training data point', fontsize=20)
plt.xlabel('Training data', fontsize=16)
plt.ylabel('Loss', fontsize=16)
plt.show()
# Plotting the average cost function over 10 training data 
pino = []
for i in range(0, 9):
 pippo = 0
 for m in range(0, 59):
 pippo+=vec_y[60*i+m]/60
 pino.append(pippo)
 
 
plt.figure(figsize=(10,6))
plt.scatter(np.arange(0, 9), pino, alpha=1, s=10, label='error')
plt.title('Average Loss by epoch', fontsize=20)
plt.xlabel('Epoch', fontsize=16)
plt.ylabel('Loss', fontsize=16)
plt.show()
def ANN_train(X_train, Y_train, p=4, q=4, eta=0.0015):
 import numpy as np
 import matplotlib.pyplot as plt
 
 # 0: Random initialize the relevant data 
 w1 = 2*np.random.rand(p , X_train.shape[1]) - 0.5 # Layer 1
 b1 = np.random.rand(p)
 w2 = 2*np.random.rand(q , p) - 0.5 # Layer 2
 b2 = np.random.rand(q)
 wOut = 2*np.random.rand(q) - 0.5 # Output Layer
 bOut = np.random.rand(1)
 mu = []
 vec_y = []
 # Start looping over the passengers, i.e. over I.
 for I in range(0, X_train.shape[0]-1): #loop in all the passengers:
 
 # 1: input the data 
 x = X_train[I]
 
 # 2: Start the algorithm
 
 # 2.1: Feed forward
 z1 = ReLU_act(np.dot(w1, x) + b1) # output layer 1 
 z2 = ReLU_act(np.dot(w2, z1) + b2) # output layer 2
 y = sigmoid_act(np.dot(wOut, z2) + bOut) # Output of the Output layer
 
 #2.2: Compute the output layer's error
 delta_Out = 2 * (y-Y_train[I]) * sigmoid_act(y, der=True)
 
 #2.3: Backpropagate
 delta_2 = delta_Out * wOut * ReLU_act(z2, der=True) # Second Layer Error
 delta_1 = np.dot(delta_2, w2) * ReLU_act(z1, der=True) # First Layer Error
 
 # 3: Gradient descent 
 wOut = wOut - eta*delta_Out*z2 # Outer Layer
 bOut = bOut - eta*delta_Out
 
 w2 = w2 - eta*np.kron(delta_2, z1).reshape(q,p) # Hidden Layer 2
 b2 = b2 - eta*delta_2
 
 w1 = w1 - eta*np.kron(delta_1, x).reshape(p, x.shape[0])
 b1 = b1 - eta*delta_1
 
 # 4. Computation of the loss function
 mu.append((y-Y_train[I])**2)
 vec_y.append(y)
 
 batch_loss = []
 for i in range(0, 10):
 loss_avg = 0
 for m in range(0, 60):
 loss_avg+=vec_y[60*i+m]/60
 batch_loss.append(loss_avg)
 
 
 plt.figure(figsize=(10,6))
 plt.scatter(np.arange(1, len(batch_loss)+1), batch_loss, alpha=1, s=10, label='error')
 plt.title('Averege Loss by epoch', fontsize=20)
 plt.xlabel('Epoch', fontsize=16)
 plt.ylabel('Loss', fontsize=16)
 plt.show()
 
 return w1, b1, w2, b2, wOut, bOut, mu
w1, b1, w2, b2, wOut, bOut, mu = ANN_train(X_train, Y_train, p=8, q=4, eta=0.0015)
def ANN_pred(X_test, w1, b1, w2, b2, wOut, bOut, mu):
 import numpy as np
 
 pred = []
 
 for I in range(0, X_test.shape[0]): #loop in all the passengers
 # 1: input the data 
 x = X_test[I]
 
 
 z1 = ReLU_act(np.dot(w1, x) + b1) # output layer 1 
 z2 = ReLU_act(np.dot(w2, z1) + b2) # output layer 2
 y = sigmoid_act(np.dot(wOut, z2) + bOut) # Output of the Output layer
 
 
 pred.append( np.heaviside(y - 0.5, 1)[0] )
 
 
 return np.array(pred)
predictions = ANN_pred(X_test, w1, b1, w2, b2, wOut, bOut, mu)
# Plot the confusion matrix
cm = confusion_matrix(Y_test, predictions)
df_cm = pd.DataFrame(cm, index = [dict_live[i] for i in range(0,2)], columns = [dict_live[i] for i in 
range(0,2)])
plt.figure(figsize = (7,7))
sns.heatmap(df_cm, annot=True, cmap=plt.cm.Blues, fmt='g')
plt.xlabel("Predicted Class", fontsize=18)
plt.ylabel("True Class", fontsize=18)
plt.show()