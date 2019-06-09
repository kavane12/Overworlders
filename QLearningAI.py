from random import random
from Network import Network
from AI import *
import math

#Learning parameters
ALPHA = 0.0002  #Learn rate
GAMMA = 0.7     #Discount factor
EPSILON = 0.9   #Chance of random action
EPS_MIN = 0.05
EPS_DECAY = 0.995
BATCH_SIZE = 2000

#Reward parameters
OFF_WEIGHT = 20     #Multiplier on the reward for doing damage
DEF_WEIGHT = 2      #Multiplier on the penalty for taking damage
ANGLE_WEIGHT = 0.5  #Multiplier on the reward for looking in the general direction of the opponent

ActionList = [
    ('move', 1), ('move', 0), ('move', -1),
    ('strafe', 1), ('strafe', 0), ('strafe', -1),
    ('turn', 1), ('turn', 0.6), ('turn', 0.4), ('turn', 0.2), ('turn', 0),
    ('turn', -0.2), ('turn', -0.4), ('turn', -0.6), ('turn', -1),
    ('pitch', 0.5), ('pitch', 0.2), ('pitch', 0.1), ('pitch', 0),
    ('pitch', -0.1), ('pitch', -0.2), ('pitch', -0.5),
    ('use', 0), ('use', 1),
    ('attack', 1),  #attack and jump are implemented as noncontinuous actions. The agent does not have to choose
    ('jump', 1),    #to stop performing them, instead they will only happen once
    ('hotbar.1', 1), ('hotbar.2', 1)
]

ActionLen = len(ActionList)
StateLen = 22

class QLearningAI(AI):
    def __init__(self, timeMult, logfile, saveNet = None, loadNet = None):
        AI.__init__(self)
        self.net = Network(StateLen, ActionLen, ALPHA, GAMMA, EPSILON, EPS_MIN, EPS_DECAY, BATCH_SIZE)
        if loadNet != None:
            self.net.load(loadNet)
        self.saveNet = saveNet
        self.counter = 0
        self.timeMult = timeMult
        self.logfile = logfile
        f = open(logfile, 'a')
        f.write("Begin log for AI with loaded net {}, saving net {}\n".format(loadNet, saveNet))
        f.close()

    def stateList(self):
        now = time.time()
        state = [
            self.life / 20,
            self.yPos,
            self.pitch / 90,
            math.cos(rad(self.opponents[0]['angle'])) * self.opponents[0]['dist'] / 10,
            math.sin(rad(self.opponents[0]['angle'])) * self.opponents[0]['dist'] / 10,
            self.opponents[0]['y'],
            math.sin(rad(self.opponents[0]['yaw'])),
            math.cos(rad(self.opponents[0]['yaw'])),
            self.opponents[0]['pitch'] / 90,
            self.opponents[0]['life'] / 20,
            self.opponents[0]['weapon'],
            self.opponents[0]['using'],
            min((now - self.opponents[0]['attackTime']) * self.timeMult, 0.5),
            (now - self.opponents[0]["useTime"]) if self.opponents[0]["using"] else 0,
            min((now - self.lastAttackTime) * self.timeMult, 0.5),
            (now - self.useStartTime) if self.using else 0,
            self.moving,
            self.strafing,
            self.turning,
            self.pitching,
            self.using,
            self.slotSelected
        ]
        assert len(state) == StateLen
        return state

    def takeAction(self, a, agentHost):
        action = ActionList[a]
        self.attacked = 0
        agentHost.sendCommand(action[0] + ' {}'.format(action[1]))
        now = time.time()
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
            self.attacked =  min((now - self.lastAttackTime) * self.timeMult, 0.5)
            self.lastAttackTime = now
        elif(action[0] == 'use'):
            self.using = action[1]
            if(action[1] == 1):
                self.useStartTime = now
        elif(action[0] == 'jump'):
            agentHost.sendCommand('jump 0')
        elif(action[0] == 'hotbar.1'):
            agentHost.sendCommand('hotbar.1 0')
            self.slotSelected = 0
            agentHost.sendCommand('use 0')
            self.using = 0
        elif(action[0] == 'hotbar.2'):
            agentHost.sendCommand('hotbar.2 0')
            self.slotSelected = 1
            agentHost.sendCommand('use 0')
            self.using = 0

    def initialize(self, agentHost):
        #additional state information
        AI.initialize(self, agentHost)
        self.moving = 0
        self.strafing = 0
        self.turning = 0
        self.pitching = 0
        self.attacked = 0
        self.lastState = None
        self.lastAction = None
        self.rewardList = []

    def run(self, agentHost):
        state = self.stateList()
        action = self.net.getAction(state)
        reward = self.calcReward()
        if self.lastState != None and self.lastAction != None:
            self.net.log(self.lastState, self.lastAction, state, reward)
        self.takeAction(action, agentHost)
        self.lastAction = action
        self.lastState = state

    def calcReward(self):
        # attackReward = 0.0

        pitchReward = .5 if abs(self.pitch) < 30 else (-5 if abs(self.pitch) > 80 else 0)
        angleReward = ANGLE_WEIGHT * ((1 - self.opponents[0]['angle'] / 30)**2 if abs(self.opponents[0]['angle']) < 30 else 0)
        #if self.attacked > 0.2:
        #     attackReward = self.attacked * 4 * distanceReward * angleReward
        # elif self.attacked != 0:
        #     attackReward = -.1

        #if self.attacked != 0:
            #print("Atk: {:6.3f} Reward: {:6.3f} DistR: {:6.3f} AnglR: {:6.3f} dist: {:5.1f} angl: {:6.1f}"
                #.format(self.attacked, attackReward, distanceReward, angleReward, self.opponents[0]['dist'], self.opponents[0]['angle']))

        combatReward = OFF_WEIGHT * (self.lastOppLife - self.opponents[0]['life']) +\
            DEF_WEIGHT * (self.life - self.lastLife)

        reward = 0.2 * (pitchReward + angleReward) + combatReward
        if pitchReward > 0:
            reward += pitchReward * angleReward

        if combatReward != 0:
            print("HIT")
            print("Combat:", combatReward, "Attack: ", self.attacked, "Time: ", time.time() - self.lastAttackTime)
        #print("Total Reward: {:8.5f} Distance: {:8.5f} Angle: {:8.5f}".format(reward, distanceReward, angleReward))
        self.rewardList.append(reward)
        return reward
    
    def finalize(self):
        self.counter += 1
        f = open(self.logfile, 'a')
        f.write("Episode {:4d}, Epsilon: {:5.3f}, Average reward: {:8.5f}, Damage done: {:4.1f}\n".format(self.counter,
            self.net.eps, sum(self.rewardList) / len(self.rewardList), 20 - self.opponents[0]['life']))
        f.close()
        for i in range(1):
            self.net.train()
        self.net.update()
        if self.saveNet != None:
            self.net.save(self.saveNet + '-' + str(self.counter) + '.dqn')

        
