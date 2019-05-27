from random import random
from Network import Network
from AI import *
import math

#Learning parameters
ALPHA = 0.001   #Learn rate
GAMMA = 0.6     #Discount factor
EPSILON = 0.3   #Chance of random action
EPS_MIN = 0.05
EPS_DECAY = 0.99
BATCH_SIZE = 2000

#Reward parameters
OFF_WEIGHT = 10  #Multiplier on the reward for doing damage
DEF_WEIGHT = .1 #Multiplier on the penalty for taking damage

ActionList = [
    ('move', 1), ('move', 0), ('move', -1),
    ('strafe', 1), ('strafe', 0), ('strafe', -1),
    ('turn', 0.5), ('turn', 0.15), ('turn', 0.05), ('turn', 0), ('turn', -0.05), ('turn', -0.15), ('turn', -0.5),
    #('pitch', 0.5), ('pitch', 0.15), ('pitch', 0.05), ('pitch', 0), ('pitch', -0.05), ('pitch', -0.15), ('pitch', -0.5),
    ('use', 0), ('use', 1),
    ('attack', 1)#,  #attack and jump are implemented as noncontinuous actions. The agent does not have to choose
    #('jump', 1)     #to stop performing them, instead they will only happen once
]

ActionLen = len(ActionList)
StateLen = 10

class QLearningAI(AI):
    def __init__(self, saveNet = None, loadNet = None):
        AI.__init__(self)
        self.net = Network(StateLen, ActionLen, ALPHA, GAMMA, EPSILON, EPS_MIN, EPS_DECAY, BATCH_SIZE)
        if loadNet != None:
            self.net.load(loadNet)
        self.saveNet = saveNet
        self.counter = 0

    def stateList(self):
        state = [
            self.life / 20,
            #self.yPos,
            #self.pitch / 90,
            self.opponents[0]['angle'] / 180,
            self.opponents[0]['dist'] / 40,
            #self.opponents[0]['y'],
            self.opponents[0]['yaw'] / 180,
            #self.opponents[0]['pitch'] / 90,
            self.opponents[0]['life'] / 20,
            time() - self.lastAttackTime,
            self.moving,
            self.strafing,
            self.turning,
            #self.pitching,
            self.using
        ]
        assert len(state) == StateLen
        return state

    def takeAction(self, a, agentHost):
        action = ActionList[a]
        agentHost.sendCommand(action[0] + ' {}'.format(action[1]))
        if(action[0] == 'move'):
            self.moving = action[1]
        elif(action[0] == 'strafe'):
            self.strafing = action[1]
        elif(action[0] == 'turn'):
            self.turning = action[1]
        elif(action[0] == 'pitch'):
            self.pitching = action[1]
        elif(action[0] == 'attack'):
            agentHost.sendCommand('attack 0')
        elif(action[0] == 'use'):
            self.using = action[1]
        elif(action[0] == 'jump'):
            agentHost.sendCommand('jump 0')

    def initialize(self, agentHost):
        #additional state information
        AI.initialize(self, agentHost)
        self.moving = 0
        self.strafing = 0
        self.turning = 0
        self.pitching = 0
        self.using = 0
        self.lastState = None
        self.lastAction = None
        self.rewardList = []

    def run(self, agentHost):
        self.counter += 1
        state = self.stateList()
        action = self.net.getAction(state)
        reward = self.calcReward()
        if self.lastState != None and self.lastAction != None:
            self.net.log(self.lastState, self.lastAction, state, reward)
        self.takeAction(action, agentHost)
        self.lastAction = action
        self.lastState = state

    def calcReward(self):
        reward = 0.0
        
        if abs(self.opponents[0]['angle']) <= 30:
            reward += (30 - abs(self.opponents[0]['angle'])) / 150

        if self.opponents[0]['dist'] < 4:
            reward += .2

        combatReward = OFF_WEIGHT * (self.lastOppLife - self.opponents[0]['life']) +\
            DEF_WEIGHT * (self.life - self.lastLife)

        if combatReward != 0:
            print("Reward:", reward, " Combat:", combatReward)
            reward += combatReward
            print("ANGLE:", self.opponents[0]['angle'])
            print("DIST :", self.opponents[0]['dist'])

        self.rewardList.append(reward)
        return reward
    
    def finalize(self):
        print(self.name, "Average reward:", sum(self.rewardList) / len(self.rewardList))
        print("Max reward:", max(self.rewardList), "Min reward:", min(self.rewardList))
        for i in range(5):
            self.net.train()
        self.net.update()
        if self.saveNet != None:
            self.net.save(self.saveNet)

        
