import json
from common import deg, angleMod, relativeAngle, relativeDistance

EPSILON = 0.3   # The chance at picking a random action
ALPHA   = 0.1   # The learning rate
GAMMA   = 1.0   # The discount factor, closer to 0 = prefers immediate rewards, closer to 1 = longterm gains

Q_TABLE_FILE = None

# NOTES FOR Q_TABLE STATES
#   myHealth: {Low, Med, High}
#   oppHealth: ^
#   
#   distance: {Close, Med, Far}
#   
#   myEquipped: {Sword, Axe, Shield} (Bow for later?)
#   oppEquipped: ^


class QLearningAI:
    def __init__(self, name):
        self.name = name
        self.life = 20
        self.opponents = {}


        # Q-table parameters
        self.epsilon = EPSILON
        self.alpha = ALPHA
        self.gamma = GAMMA
        
        self.q_table = {}
        if Q_TABLE_FILE:
            with open(Q_TABLE_FILE) as f:
                self.q_table = json.load(f)


    def initialize(self, agentHost):
        equippedShield = False

        if not equippedShield:
            worldState = agentHost.getWorldState()
            if worldState.number_of_observations_since_last_state > 0:
                agentHost.sendCommand("chat " + "/replaceitem entity " + self.name + " slot.weapon.offhand minecraft:shield")
                equippedShield = True
            else:
                return False

        return True


    def act(self, agentHost):
        worldState = agentHost.getWorldState()

        if worldState.number_of_observations_since_last_state > 0:

            obs = json.loads(worldState.observations[-1].text)

            self.life = obs["Life"]
            xPos = obs["XPos"]
            yPos = obs["YPos"]
            zPos = obs["ZPos"]
            pitch = obs["Pitch"]
            yaw = obs["Yaw"]
            entities = obs["entities"]

            for e in entities:
                name = e['name']
                if name != self.name:       # Will not see the Observer due to y limit on entity observation
                    dx = e['x'] - xPos
                    dz = e['z'] - zPos
                    a = deg(relativeAngle(dx, dz))
                    self.opponents[name] = {
                        'angle':angleMod(a - yaw),          # Angle to opponent in degrees, positive is clockwise
                        'dist': relativeDistance(dx, dz),   # Horizontal distance to opponent
                        'y':e['y'],                         # Vertical position of oppoent
                        'yaw':angleMod(e['yaw'] - a + 180), # Relative yaw of opponent (0 = looking towards agent, 90 = looking to the right of agent, -90 = looking to the left)              
                        'pitch':e['pitch'],
                        'life':e['life'],
                    }
            #if(self.name == 'Player_1'):
                #o = self.opponents['Player_2']
                #print(o['angle'], o['dist'], o['yaw'], o['y']) #debug code
            if self.life <= 0:
                return False

            
        return True
