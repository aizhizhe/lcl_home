class Node:
    """
    Each node in neural networks will have these attributes and methods
    """

    def __init__(self, inputs=[]):
        """
        if the node is the operator of "ax + b", the inputs will be x node , and the outputs
        of this is its successors.

        and the value is *ax + b*
        """
        self.inputs = inputs  # input_list <- C, Java <- 匈牙利命名法 -> Python 特别不建议
        # self.outputs = outputs # output_list
        self.value = None
        self.outputs = []
        self.gradients = {}

        for node in self.inputs:
            node.outputs.append(self)  # build a connection relationship

    def forward(self):
        """Forward propogation

        compute the output value based on input nodes and store the value
        into *self.value*
        """
        raise NotImplemented

    def backward(self):
        """ Back propogation

        compute the gradient of each input node and store the value
        into "self.gredients"
        """
        raise NotImplemented




class Input(Node):
    def __init__(self, name=''):
        Node.__init__(self, inputs=[])
        self.name = name

    def forward(self, value=None):
        if value is not None:
            self.value = value

    def backward(self):
        self.gradients = {}
        for n in self.outputs:
            grad_cost = n.gradients[self]
            self.gradients[self] = grad_cost
            # print(self.gradients[self])
    def __repr__(self):
        return 'Input Node: {}'.format(self.name)


class Linear(Node):
    def __init__(self, nodes, weights, bias):
        self.w_node = weights
        self.x_node = nodes
        self.b_node = bias
        Node.__init__(self, inputs=[nodes, weights, bias])

    def forward(self):
        """compute the wx + b using numpy"""
        self.value = np.dot(self.x_node.value, self.w_node.value) + self.b_node.value

    def backward(self):
        for node in self.outputs:
            # gradient_of_loss_of_this_output_node = node.gradient[self]
            grad_cost = node.gradients[self]

            self.gradients[self.w_node] = np.dot(self.x_node.value.T, grad_cost)
            self.gradients[self.b_node] = np.sum(grad_cost * 1, axis=0, keepdims=False)
            self.gradients[self.x_node] = np.dot(grad_cost, self.w_node.value.T)


class Sigmoid(Node):
    def __init__(self, node):
        Node.__init__(self, [node])
        self.x_node = node

    def _sigmoid(self, x):
        return 1. / (1 + np.exp(-1 * x))

    def forward(self):
        self.value = self._sigmoid(self.x_node.value)

    def backward(self):
        y = self.value

        self.partial = y * (1 - y)

        for n in self.outputs:
            grad_cost = n.gradients[self]

            self.gradients[self.x_node] = grad_cost * self.partial


class MSE(Node):
    def __init__(self, y_true, y_hat):
        self.y_true_node = y_true
        self.y_hat_node = y_hat
        Node.__init__(self, inputs=[y_true, y_hat])

    def forward(self):
        y_true_flatten = self.y_true_node.value.reshape(-1, 1)
        y_hat_flatten = self.y_hat_node.value.reshape(-1, 1)

        self.diff = y_true_flatten - y_hat_flatten

        self.value = np.mean(self.diff ** 2)

    def backward(self):
        n = self.y_hat_node.value.shape[0]

        self.gradients[self.y_true_node] = (2 / n) * self.diff
        self.gradients[self.y_hat_node] = (-2 / n) * self.diff


def training_one_batch(topological_sorted_graph):
    # graph 是经过拓扑排序之后的 一个list
    for node in topological_sorted_graph:
        node.forward()

    for node in topological_sorted_graph[::-1]:
        node.backward()


def topological_sort(data_with_value):
    feed_dict = data_with_value
    input_nodes = [n for n in feed_dict.keys()]

    G = {}
    nodes = [n for n in input_nodes]
    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in G:
            G[n] = {'in': set(), 'out': set()}
        for m in n.outputs:
            if m not in G:
                G[m] = {'in': set(), 'out': set()}
            G[n]['out'].add(m)
            G[m]['in'].add(n)
            nodes.append(m)

    L = []
    S = set(input_nodes)
    while len(S) > 0:
        n = S.pop()

        if isinstance(n, Input):
            n.value = feed_dict[n]
            ## if n is Input Node, set n'value as
            ## feed_dict[n]
            ## else, n's value is caculate as its
            ## inbounds

        L.append(n)
        for m in n.outputs:
            G[n]['out'].remove(m)
            G[m]['in'].remove(n)
            # if no other incoming edges add to S
            if len(G[m]['in']) == 0:
                S.add(m)
    return L



def sgd_update(trainable_nodes, learning_rate=1e-2):
    for t in trainable_nodes:
        t.value += -1 * learning_rate * t.gradients[t]


from sklearn.datasets import load_boston
import numpy as np
data = load_boston()
X_ = data['data']
print(X_)

y_ = data['target']
print(y_)
X_ = (X_ - np.mean(X_, axis=0)) / np.std(X_, axis=0)
n_features = X_.shape[1]
n_hidden = 10
n_hidden_2 = 10
W1_, b1_ = np.random.randn(n_features, n_hidden), np.zeros(n_hidden)
W2_, b2_ = np.random.randn(n_hidden, 1), np.zeros(1)

X, y = Input(name='X'), Input(name='y')  # tensorflow -> placeholder
W1, b1 = Input(name='W1'), Input(name='b1')
W2, b2 = Input(name='W2'), Input(name='b2')
# W3, b3 = Input(name='W3'), Input(name='b3')
print(X.outputs)
linear_output = Linear(X, W1, b1)
print(X.outputs)
print(W1.outputs)
print(b1.outputs)
sigmoid_output = Sigmoid(linear_output)
yhat = Linear(sigmoid_output, W2, b2)
loss = MSE(y, yhat)

input_node_with_value = {
    X: X_,
    y: y_,
    W1: W1_,
    W2: W2_,
    b1: b1_,
    b2: b2_
}

graph = topological_sort(input_node_with_value)

from sklearn.utils import resample

def run(dictionary):
    return topological_sort(dictionary)


losses = []
epochs = 5000

batch_size = 64

steps_per_epoch = X_.shape[0] // batch_size

for i in range(epochs):
    loss = 0

    for batch in range(steps_per_epoch):
        # indices = np.random.choice(range(X_.shape[0]), size=10, replace=True)
        # X_batch = X_[indices]
        # y_batch = y_[indices]
        X_batch, y_batch = resample(X_, y_, n_samples=batch_size)

        X.value = X_batch
        y.value = y_batch

        #         input_node_with_value = {  # -> feed_dict
        #             X: X_batch,
        #             y: y_batch,
        #             W1: W1.value,
        #             W2: W2.value,
        #             b1: b1.value,
        #             b2: b2.value,
        #         }

        #         graph = topological_sort(input_node_with_value)

        training_one_batch(graph)

        learning_rate = 1e-3

        sgd_update(trainable_nodes=[W1, W2, b1, b2], learning_rate=learning_rate)

        loss += graph[-1].value

    if i % 100 == 0:
        print('Epoch: {}, loss = {:.3f}'.format(i + 1, loss / steps_per_epoch))
        losses.append(loss)

import matplotlib.pyplot as plt
plt.plot(losses)