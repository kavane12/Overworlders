from random import random
from Network import Network
from AI import *
import math

#Learning parameters
ALPHA = 0.0004  #Learn rate
GAMMA = 0.9     #Discount factor
EPSILON = 0.35  #Chance of random action
EPS_MIN = 0.05
EPS_DECAY = 0.985
BATCH_SIZE = 2000

#Reward parameters
OFF_WEIGHT = 20     #Multiplier on the reward for doing damage
DEF_WEIGHT = 2      #Multiplier on the penalty for taking damage

ActionList = [
    ('move', 1), ('move', 0), ('move', -1),
    ('strafe', 1), ('strafe', 0), ('strafe', -1),
    ('turn', 1), ('turn', 0.6), ('turn', 0.25), ('turn', 0.1), ('turn', 0), ('turn', -0.1), ('turn', -0.25), ('turn', -0.6), ('turn', -1),
    ('pitch', 0.4), ('pitch', 0.15), ('pitch', 0.05), ('pitch', 0), ('pitch', -0.05), ('pitch', -0.15), ('pitch', -0.4),
    ('jump', 1),    #perform a single jump
    ('attack', 1),  #switch to the sword and perform a single attack
    ('block', 0), ('block', 1), #switch to the sword & shield, and start/stop blocking
    ('shoot', 0), ('shoot', 1)  #switch to the bow and draw (1) or shoot (0, if already drawing)
]

ActionLen = len(ActionList)
StateLen = 26

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
            self.moving,
            self.strafing,
            self.turning,
            self.pitching,
            self.blocking,
            self.drawing,
            self.timeSince(self.lastAttackTime, limit = 0.6),
            self.timeSince(self.drawStartTime, condition = self.drawing),
            self.life / 20,
            self.yPos,
            self.pitch / 90,
            math.cos(rad(self.opponents[0]['angle'])) * self.opponents[0]['dist'] / 10,
            math.sin(rad(self.opponents[0]['angle'])) * self.opponents[0]['dist'] / 10,
            self.opponents[0]['moving'],
            self.opponents[0]['strafing'],
            self.opponents[0]['turning'],
            self.opponents[0]['pitching'],
            self.opponents[0]['blocking'],
            self.opponents[0]['drawing'],
            self.timeSince(self.opponents[0]['attackTime'], limit = 0.6),
            self.timeSince(self.opponents[0]["drawTime"], condition = self.opponents[0]["drawing"]),
            self.opponents[0]['life'] / 20,
            self.opponents[0]['y'],
            self.opponents[0]['pitch'] / 90,
            math.sin(rad(self.opponents[0]['yaw'])),
            math.cos(rad(self.opponents[0]['yaw']))
        ]
        assert len(state) == StateLen
        return state

    def takeAction(self, a, agentHost):
        if len(self.queuedCommands) > 0:
            for c in self.queuedCommands:
                agentHost.sendCommand(c)
            self.queuedCommands = []
        action = ActionList[a]
        self.attacked = 0
        self.shot = 0
        if action[0] in ['move', 'strafe', 'turn', 'pitch', 'jump']:
            agentHost.sendCommand(action[0] + ' {}'.format(action[1]))
        if(action[0] == 'move'):
            self.moving = action[1]
        elif(action[0] == 'strafe'):
            self.strafing = action[1]
        elif(action[0] == 'turn'):
            self.turning = action[1]
        elif(action[0] == 'pitch'):
            self.pitching = action[1]
        elif(action[0] == 'jump'):
            agentHost.sendCommand('jump 0')
        elif(action[0] == 'attack'):
            self.attacked = self.timeSince(self.lastAttackTime, limit = 0.6)
            if self.attacked > 0.2:
                if self.drawing:
                    agentHost.sendCommand('use 0')
                    agentHost.sendCommand('hotbar.1 1')
                    agentHost.sendCommand('hotbar.1 0')
                    self.queuedCommands.append('attack 1')
                    self.queuedCommands.append('attack 0')
                    self.drawing = 0
                    self.shot = self.timeSince(self.drawStartTime)
                elif self.blocking:
                    self.blocking = 0
                    agentHost.sendCommand('use 0')
                    self.queuedCommands.append('attack 1')
                    self.queuedCommands.append('attack 0')
                else:
                    agentHost.sendCommand('attack 1')
                    agentHost.sendCommand('attack 0')
                self.lastAttackTime = time.time()
        elif(action[0] == 'block'):
            if self.drawing:
                agentHost.sendCommand('use 0')
                agentHost.sendCommand('hotbar.1 1')
                agentHost.sendCommand('hotbar.1 0')
                self.drawing = 0
                self.shot = self.timeSince(self.drawStartTime)
                self.queuedCommands.append('use {}'.format(action[1]))
                self.blocking = action[1]
            elif self.blocking != action[1]:
                agentHost.sendCommand('use {}'.format(action[1]))
                self.blocking = action[1]
        elif(action[0] == 'shoot'):
            if action[1] == 1 and not self.drawing:
                agentHost.sendCommand('hotbar.2 1')
                agentHost.sendCommand('hotbar.2 0')
                if self.blocking:
                    agentHost.sendCommand('use 0')
                    self.blocking = 0
                    self.queuedCommands.append('use 1')
                else:
                    agentHost.sendCommand('use 1')
                self.drawStartTime = time.time()
                self.drawing = 1
            elif action[1] == 0 and self.drawing:
                agentHost.sendCommand('use 0')
                agentHost.sendCommand('hotbar.1 1')
                agentHost.sendCommand('hotbar.1 0')
                self.drawing = 0
                self.shot = self.timeSince(self.drawStartTime)

    def initialize(self, agentHost):
        AI.initialize(self, agentHost)
        self.queuedCommands = []
        
        #information for replay memory/rewards
        self.attacked = 0
        self.shot = 0
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
        attackReward = 0.0
        shotReward = 0.0
        drawReward = 0.0
        
        pitchPenalty = -5 if abs(self.pitch) > 60 else 0
        pitchReward = 1 if abs(self.pitch) < 30 else 0
        angleReward = (1 - abs(self.opponents[0]['angle']) / 45)**2 if abs(self.opponents[0]['angle']) < 45 else 0

        if self.attacked > 0:
            if self.opponents[0]['dist'] < 3.7:
                if self.attacked > 0.2:
                    attackReward = self.attacked * 2 * pitchReward * angleReward
                else:
                    attackReward = -.1
            elif self.opponents[0]['dist'] > 5:
                attackReward = -.5

            print("{} Atk: {:6.3f} Reward: {:6.3f} dist: {:5.1f} angl: {:6.1f} pitch: {:6.1f}"
                .format(self.name, self.attacked, attackReward, self.opponents[0]['dist'],
                        self.opponents[0]['angle'], self.pitch))

        shotPitchReward = (1 - abs(self.pitch + 2) / 30)**2 if abs(self.pitch + 2) < 30 else 0
        
        if self.drawing:
            if self.timeSince(self.drawStartTime) < .95 and self.opponents[0]['dist'] > 5:
                drawReward = 3 * angleReward * shotPitchReward
                
        if self.shot > 0.3:
            if self.opponents[0]['dist'] >= 5:
                shotReward = self.shot * 6 * angleReward * shotPitchReward
        elif self.shot != 0:
            shotReward = -.1

        if self.shot != 0:
            print("{} Shot: {:6.3f} Reward: {:6.3f} dist: {:5.1f} angl: {:6.1f} pitch: {:6.1f}"
                .format(self.name, self.shot, shotReward, self.opponents[0]['dist'],
                        self.opponents[0]['angle'], self.pitch))
        
        combatReward = OFF_WEIGHT * (self.lastOppLife - self.opponents[0]['life']) +\
            DEF_WEIGHT * (self.life - self.lastLife)

        reward = 0.2 * (pitchReward + angleReward) + pitchReward * angleReward + pitchPenalty +\
            combatReward + attackReward + shotReward + drawReward

        if combatReward != 0:
            print("{} HIT: {}".format(self.name, combatReward))
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

    def timeSince(self, t, limit = 1, condition = True):
        return (min(limit, self.timeMult * (time.time() - t)) / limit) if condition else 0
