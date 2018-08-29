import numpy as np
from scipy.special import expit

class Model:
    input_size = 25
    layer1_size = 16
    layer2_size = 1

    def __init__(self):
        self.layer1 = 2 * np.random.rand(Model.input_size, Model.layer1_size) - 1
        self.layer2 = 2 * np.random.rand(Model.layer1_size, Model.layer2_size) - 1
        self.b1 = 2 * np.random.rand(1, Model.layer1_size) - 1
        self.b2 = 2 * np.random.rand(1, Model.layer2_size) - 1

    @staticmethod
    def from_weights(layer1, layer2):
        m = Model()
        m.layer1 = layer1
        m.layer2 = layer2
        return m

    def get_action(self, state):
        z1 = Model.activation(state.T.dot(self.layer1) + self.b1)
        z2 = Model.activation(z1.dot(self.layer2) + self.b2)
        return z2

    def get_weights(self):
        return self.layer1, self.layer2

    def mutate(self):
        return Model.from_weights(self.layer1, self.layer2)

    @staticmethod
    def combine(m1, m2):
        pass

    @staticmethod
    def activation(x):
        return np.tanh(x)



