from AI import *

    # Parameters:
attackSpeed = 1.7   # Max attacks per second
shotSpeed = .5       # Max bow shots per second
turnAngle = 60      # Angle at which agent will turn at full speed. If set too low, agent will oscillate
moveDist = 4.5      # Below this threshold, agent will move toward opponent for melee combat, above, it will back away and shoot
attackAngle = 10    # Maximum angle at which agent will try to attack
attackDist = 3.7    # Maximum distance at which agent will try to attack

class BasicAI(AI):
    def run(self, agentHost):          
        enemy = self.opponents[0]
        targetPitch = -15 * (enemy['dist'] - attackDist) if enemy['dist'] < attackDist else -(enemy['dist'] / 15)**2
        self.turning = enemy['angle'] / turnAngle if abs(enemy['angle']) < turnAngle else (1 if enemy['angle'] > 0 else -1)
        self.pitching = (targetPitch - self.pitch) / 180
        if enemy['dist'] < moveDist and not self.drawing:
            if enemy['dist'] > attackDist:
                self.moving = 1
            else:
                self.moving = 0
                if time.time() - self.lastAttackTime > 1 / attackSpeed and abs(enemy['angle']) < attackAngle:
                    agentHost.sendCommand("attack 1")
                    agentHost.sendCommand("attack 0")
                    self.lastAttackTime = time.time()                    
        else:
            self.moving = 0
            if not self.drawing:
                self.drawing = 1
                agentHost.sendCommand("hotbar.2 1")
                agentHost.sendCommand("hotbar.2 0")
                agentHost.sendCommand("use 1")
                self.drawStartTime = time.time()
            elif enemy['dist'] < attackDist or (time.time() - self.drawStartTime >= 1 / shotSpeed and abs(enemy['angle']) < attackAngle / 2):
                agentHost.sendCommand("use 0")
                agentHost.sendCommand("hotbar.1 1")
                agentHost.sendCommand("hotbar.1 0")
                self.drawing = 0
        agentHost.sendCommand("pitch {}".format(self.pitching))
        agentHost.sendCommand("turn {}".format(self.turning))
        agentHost.sendCommand("move {}".format(self.moving))

