import json
from common import deg, angleMod, relativeAngle, relativeDistance

class PassiveAI:
    def __init__(self, name):
        self.name = name
        self.life = 20
        self.opponents = {}
        

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

            if self.life <= 0:
                return False

            self.faceOpponent(agentHost)
            
        return True

    def faceOpponent(self, agentHost):
        turnAngle = 80      # Angle at which agent will turn at full speed. If set too low, agent will oscillate

        enemy = list(self.opponents.values())[0]
        turnSpd = enemy['angle'] / turnAngle if abs(enemy['angle']) < turnAngle else (1 if enemy['angle'] > 0 else -1)
        agentHost.sendCommand("turn {}".format(turnSpd))