import json
import time

from common import deg, rad, angleMod, relativeAngle, relativeDistance
#from time import time

class AI:
    def __init__(self):
        #State elements
        self.life = 20
        self.yPos = 0
        self.pitch = 0
        self.opponents = []
        
    def initialize(self, agentHost):
        #Previous state info (for calculating rewards)
        self.lastLife = 20
        self.lastOppLife = 20

        #state info
        self.moving = 0
        self.strafing = 0
        self.turning = 0
        self.pitching = 0
        self.blocking = 0
        self.drawing = 0
        
        worldState = agentHost.getWorldState()
        while worldState.number_of_observations_since_last_state <= 0:
            worldState = agentHost.getWorldState()
        obs = json.loads(worldState.observations[-1].text)
        self.name = obs["Name"]
        agentHost.sendCommand("hotbar.3 1")
        agentHost.sendCommand("hotbar.3 0")
        time.sleep(1)
        agentHost.sendCommand("swapHands 1")
        agentHost.sendCommand("swapHands 0")
        agentHost.sendCommand("hotbar.1 1")
        agentHost.sendCommand("hotbar.1 0")
        agentHost.sendCommand("sprint 1")

        #additional info
        self.drawStartTime = time.time()
        self.lastAttackTime = time.time()
        
    def finalize(self):   #virtual function for any code that needs to be run on mission end
        pass

    def run(self, agentHost):   #virtual function where an AI's behavior should be implemented
        pass

    def act(self, agentHost, AIs):
        worldState = agentHost.getWorldState()
        if worldState.number_of_observations_since_last_state > 0:
            obs = json.loads(worldState.observations[-1].text)
            self.life = obs["Life"]
            if self.life <= 0:
                return False
            self.xPos = obs["XPos"]
            self.yPos = obs["YPos"] - 200
            self.zPos = obs["ZPos"]
            self.pitch = obs["Pitch"]
            yaw = obs["Yaw"]
            entities = obs["entities"]
            self.opponents = []
            for e in entities:
                name = e['name']
                if name.startswith("Player") and name != self.name:  # Must check that name starts with player, or else item entities will be picked up
                    dx = e['x'] - self.xPos
                    dz = e['z'] - self.zPos
                    a = deg(relativeAngle(dx, dz))
                    self.opponents.append({
                        'name':name,
                        'angle':angleMod(a - yaw),          # Angle to opponent in degrees, positive is clockwise
                        'dist': relativeDistance(dx, dz),   # Horizontal distance to opponent
                        'y':e['y'] - 200,                   # Vertical position of oppoent
                        'yaw':angleMod(e['yaw'] - a + 180), # Relative yaw of opponent (0 = looking towards agent, 90 = looking to the right of agent, -90 = looking to the left)              
                        'pitch':e['pitch'],
                        'life':e['life'],
                        'x':e['x'],
                        'z':e['z']
                    })
                    for ai in AIs:
                        if ai.name == name:
                            self.opponents[-1]['moving'] = ai.moving
                            self.opponents[-1]['strafing'] = ai.strafing
                            self.opponents[-1]['turning'] = ai.turning
                            self.opponents[-1]['pitching'] = ai.pitching
                            self.opponents[-1]['blocking'] = ai.blocking
                            self.opponents[-1]['drawing'] = ai.drawing
                            self.opponents[-1]['attackTime'] = ai.lastAttackTime
                            self.opponents[-1]['drawTime'] = ai.drawStartTime
                            break
            self.opponents.sort(key = lambda x:x['dist'])
            self.run(agentHost)
            self.lastLife = self.life
            self.lastOppLife = self.opponents[0]['life']
        return True
