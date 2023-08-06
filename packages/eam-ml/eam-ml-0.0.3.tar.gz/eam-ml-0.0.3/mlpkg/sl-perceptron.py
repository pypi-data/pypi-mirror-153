
from itertools import cycle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

train_data = np.array([[0, 0],[0, 1],[1, 0],[1, 1]])


target_and = np.array([[0],[0],[0],[1]])
target_or = np.array([[0],[1],[1],[1]])
target_nand = np.array([[1],[1],[1],[0]])
target_xor = np.array([[0],[1],[1],[0]])

class Perceptron:

    def __init__(self, train_data, target, lr=0.01, input_nodes=2):
        self.train_data = train_data
        self.target = target
        self.lr = lr
        self.input_nodes = input_nodes
        self.w = np.random.uniform(size=self.input_nodes)
        self.b = -1

        self.node_val = np.zeros(self.input_nodes)
        self.correct_iter = [0]

    def _gradient(self, node, exp, output):
        return node * (exp - output)

    def update_weights(self, exp, output):

        for i in range(self.input_nodes):
            self.w[i] += self.lr * self._gradient(self.node_val[i], exp, output)

        self.b += self.lr * self._gradient(1, exp, output)

    def forward(self, datapoint):
        return self.b + np.dot(self.w, datapoint)

    def classify(self, datapoint):
        if self.forward(datapoint) >= 0:
            return 1

        return 0

    def plot(self, h=0.01):
        sns.set_style('darkgrid')
        plt.figure(figsize=(10, 10))

        plt.axis('scaled')
        plt.xlim(-0.1, 1.1)
        plt.ylim(-0.1, 1.1)

        colors = {
            0: "ro",
            1: "go"
        }

        for i in range(len(self.train_data)):
            plt.plot([self.train_data[i][0]],
                     [self.train_data[i][1]],
                     colors[self.target[i][0]],
                     markersize=20)

        x_range = np.arange(-0.1, 1.1, h)
        y_range = np.arange(-0.1, 1.1, h)

        xx, yy = np.meshgrid(x_range, y_range, indexing='ij')
        Z = np.array([[self.classify([x, y]) for x in x_range] for y in y_range])

        plt.contourf(xx, yy, Z, colors=['red', 'green', 'green', 'blue'], alpha=0.4)
        plt.show(block=True)

    def train(self):
        correct_counter = 0
        iterations = 0

        for train, target in cycle(zip(self.train_data, self.target)):

            if correct_counter == len(self.train_data):
                break

            if iterations > 1000:
                print("1000 iterations exceded without convergence! A single layered perceptron can't handle the XOR problem.")
                break

            output = self.classify(train)
            self.node_val = train
            iterations += 1

            if output == target:
                correct_counter += 1
            else:
                self.update_weights(target, output)
                correct_counter = 0
        
            self.correct_iter.append(correct_counter)

# AND PERCEPTRON        
p_and = Perceptron(train_data, target_and)
p_and.train()
_ = plt.plot(p_and.correct_iter[:1000])
plt.show(block=True)
p_and.plot()

# OR PERCEPTRON        
p_or = Perceptron(train_data, target_or)
p_or.train()
_ = plt.plot(p_or.correct_iter[:1000])
plt.show(block=True)
p_or.plot()

# NAND PERCEPTRON        
p_nand = Perceptron(train_data, target_nand)
p_nand.train()
_ = plt.plot(p_nand.correct_iter[:1000])
plt.show(block=True)
p_nand.plot()

# XOR PERCEPTRON        
p_xor = Perceptron(train_data, target_xor)
p_xor.train()
_ = plt.plot(p_xor.correct_iter[:200])
plt.show(block=True)
p_xor.plot()