import numpy as np
import random
from car import Car


class Model:
    input_size = (Car.matrix_size*2 + 1)**2
    layer1_size = 8
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

    def getJSON(self):
        return {
            "layer1": self.layer1.toList(),
            "layer2": self.layer2.toList(),
            "bias1": self.b1.toList(),
            "bias2": self.b2.toList()
        }

    def mutate(self):
        if np.random.rand() < 0.5:
            self.layer1 = 2 * np.random.rand(Model.input_size, Model.layer1_size) - 1
        else:
            self.layer2 = 2 * np.random.rand(Model.layer1_size, Model.layer2_size) - 1

    @staticmethod
    def activation(x):
        return np.tanh(x)

    @staticmethod
    def combine(m1, m2):
        m = Model()

        for i in range(m1.layer1.shape[0]):
            if np.random.rand() < 0.5:
                m.layer1[i] = m1.layer1[i]
            else:
                m.layer1[i] = m2.layer1[i]

        for i in range(m1.layer2.shape[0]):
            if np.random.rand() < 0.5:
                m.layer2[i] = m1.layer2[i]
            else:
                m.layer2[i] = m2.layer2[i]

        return m

    @staticmethod
    def combine_random(m1, m2):
        m = Model()

        for i in range(m1.layer1.shape[0]):
            for j in range(m1.layer1.shape[1]):
                if np.random.rand() < 0.5:
                    m.layer1[i, j] = m1.layer1[i, j]
                else:
                    m.layer1[i, j] = m2.layer1[i, j]

        for i in range(m1.layer2.shape[0]):
            for j in range(m1.layer2.shape[1]):
                if np.random.rand() < 0.5:
                    m.layer2[i, j] = m1.layer2[i, j]
                else:
                    m.layer2[i, j] = m2.layer2[i, j]

        return m
