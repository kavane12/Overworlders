from tensorflow import keras
import numpy as np
import random
from collections import deque

class Network:
    def __init__(self, numInputs, numOutputs, lr, gamma, eps, epsMin, epsDecay, batchSize):
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.memory = deque(maxlen = 50000)
        self.lr = lr
        self.gamma = gamma
        self.eps = eps
        self.epsMin = epsMin
        self.epsDecay = epsDecay
        self.batchSize = batchSize
        self.policyNet = self.buildModel(numInputs, numOutputs)
        self.targetNet = self.buildModel(numInputs, numOutputs)
        self.update()
        self.counter = 0

    def buildModel(self, numInputs, numOutputs):
        model = keras.Sequential()
        model.add(keras.layers.Dense(numInputs * 3, input_dim = numInputs, activation='relu'))
        model.add(keras.layers.Dense(numInputs * 2 + numOutputs, activation='relu'))
        model.add(keras.layers.Dense(numInputs + 2 * numOutputs, activation='relu'))
        model.add(keras.layers.Dense(3 * numOutputs, activation='relu'))
        model.add(keras.layers.Dense(numOutputs, activation = 'linear'))
        model.compile(loss='mse', optimizer = keras.optimizers.Adam(lr = self.lr))
        return model

    def update(self):
        self.targetNet.set_weights(self.policyNet.get_weights())

    def log(self, state, action, nextState, reward, done = False):
        self.memory.append((np.reshape(state, [1, self.numInputs]), action, np.reshape(nextState, [1, self.numInputs]), reward, done))

    def getAction(self, state):
        actionVals = self.policyNet.predict(np.reshape(state, [1, self.numInputs]))
        if self.counter % 2000 == 0:
            print(self.eps, actionVals, sep = '\n')
        self.counter += 1
        if np.random.rand() < self.eps:
            return random.randrange(self.numOutputs)
        return np.argmax(actionVals[0])

    def train(self):
        if len(self.memory) < self.batchSize:
            return
        batch = random.sample(self.memory, self.batchSize)
        for state, action, nextState, reward, done in batch:
            qStar = reward
            if not done:
                qStar += self.gamma * np.amax(self.targetNet.predict(nextState)[0])
            q = self.policyNet.predict(state)
            q[0][action] = qStar
            self.policyNet.fit(state, q, epochs = 1, verbose = 0)
        if self.eps > self.epsMin:
            self.eps *= self.epsDecay

    def save(self, path):
        self.policyNet.save(path)

    def load(self, path):
        self.policyNet = keras.models.load_model(path)
        self.update()
