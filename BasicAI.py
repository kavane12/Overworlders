import json
from common import deg, angleMod, relativeAngle, relativeDistance

class BasicAI:
    def __init__(self, name):
        self.name = name
        self.life = 20
        self.opponents = {}
        self.equippedShield = False
        

    def act(self, agentHost):
        worldState = agentHost.getWorldState()

        if worldState.number_of_observations_since_last_state > 0:

            if not self.equippedShield:
                agentHost.sendCommand("chat " + "/replaceitem entity " + self.name + " slot.weapon.offhand minecraft:shield")
                self.equippedShield = True

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

            self.attackOpponent(agentHost)
            
        return True

    def attackOpponent(self, agentHost):
                            # Parameters:
        turnAngle = 80      # Angle at which agent will turn at full speed. If set too low, agent will oscillate
        moveDist = 3        # Agent will try to stay within this distance of enemy
        attackAngle = 10    # Maximum angle at which agent will try to attack
        attackDist = 3.5    # Maximum distance at which agent will try to attack

        enemy = list(self.opponents.values())[0]
        turnSpd = enemy['angle'] / turnAngle if abs(enemy['angle']) < turnAngle else (1 if enemy['angle'] > 0 else -1)
        agentHost.sendCommand("turn {}".format(turnSpd))
        agentHost.sendCommand("move {}".format(1 if enemy['dist'] > moveDist else 0))
        agentHost.sendCommand("attack {}".format(1 if abs(enemy['angle']) < attackAngle and enemy['dist'] < attackDist else 0))

