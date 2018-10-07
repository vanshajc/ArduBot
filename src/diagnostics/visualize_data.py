#!/usr/local/bin/python3.6
import numpy as np
import json
import sys
import matplotlib.pyplot as plt
import config
from model import *


def main():
    with open(sys.argv[1], 'r') as f:
        dict = json.load(f)

    l1 = np.array(dict["layer1"])
    b1 = np.array(dict["bias1"])
    l2 = np.array(dict["layer2"])
    b2 = np.array(dict["bias2"])

    m = Model.get_model(l1, b1, l2, b2)
    m2 = Model()

    print(m.get_action(np.expand_dims(config.lu.flatten(), axis=1)))
    print(m.get_action(np.expand_dims(config.ru.flatten(), axis=1)))
    print(m.get_action(np.expand_dims(config.up.flatten(), axis=1)))
    print(m.get_action(np.expand_dims(config.dn.flatten(), axis=1)))


if __name__ == '__main__':
    main()
