import json
import math

def deg(angle):
    return angle * 180 / math.pi

def rad(angle):
    return angle * math.pi / 180

def angleMod(angle):    #converts an angle to a value between -180 and 180 degrees
    angle %= 360
    if angle > 180:
        angle -= 360
    return angle

class AI:
    def __init__(self, name, aiType = "passive"):
        self.name = name
        self.life = 20
        self.aiType = aiType
        self.opponents = {}
        self.equippedShield = False
        

    def act(self, agentHost):
        worldState = agentHost.getWorldState()
        
        if worldState.number_of_observations_since_last_state > 0:

            if not self.equippedShield:
                self.equippedShield = True
                agentHost.sendCommand("chat " + "/replaceitem entity " + self.name + " slot.weapon.offhand minecraft:shield")

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
                if name != self.name and name.startswith("Player"):
                    dx = e['x'] - xPos
                    dz = e['z'] - zPos
                    a = deg(-math.atan2(dx, dz))
                    self.opponents[name] = {
                        'angle':angleMod(a - yaw),          #angle to opponent in degrees, positive is clockwise
                        'dist':math.sqrt(dx**2 + dz**2),    #horizontal distance to opponent
                        'y':e['y'],                         #vertical position of oppoent
                        'yaw':angleMod(e['yaw'] - a + 180), #relative yaw of opponent (0 = looking towards agent, 90 = looking to the right of agent, -90 = looking to the left)              
                        'pitch':e['pitch'],
                        'life':e['life'],
                    }
            #if(self.name == 'Player_1'):
                #o = self.opponents['Player_2']
                #print(o['angle'], o['dist'], o['yaw'], o['y']) #debug code
            if self.life <= 0:
                return False
            if self.aiType == 'basic':
                self.basicAI(agentHost)
            
        return True

    def basicAI(self, agentHost):
                            #parameters:
        turnAngle = 80      #angle at which agent will turn at full speed. If set too low, agent will oscillate
        moveDist = 3      #agent will try to stay within this distance of enemy
        attackAngle = 10    #maximum angle at which agent will try to attack
        attackDist = 3.5      #maximum distance at which agent will try to attack

        enemy = list(self.opponents.values())[0]
        turnSpd = enemy['angle'] / turnAngle if abs(enemy['angle']) < turnAngle else (1 if enemy['angle'] > 0 else -1)
        agentHost.sendCommand("turn {}".format(turnSpd))
        agentHost.sendCommand("move {}".format(1 if enemy['dist'] > moveDist else 0))
        agentHost.sendCommand("attack {}".format(1 if abs(enemy['angle']) < attackAngle and enemy['dist'] < attackDist else 0))

