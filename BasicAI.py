from AI import *

    # Parameters:
attackSpeed = 1.5   # Max attacks per second
turnAngle = 80      # Angle at which agent will turn at full speed. If set too low, agent will oscillate
moveDist = 3        # Agent will try to stay within this distance of enemy
attackAngle = 10    # Maximum angle at which agent will try to attack
attackDist = 3.5    # Maximum distance at which agent will try to attack

class BasicAI(AI):
    def run(self, agentHost):          
        enemy = self.opponents[0]
        doAttack = time() - self.lastAttackTime > 1 / attackSpeed and abs(enemy['angle']) < attackAngle and enemy['dist'] < attackDist
        turnSpd = enemy['angle'] / turnAngle if abs(enemy['angle']) < turnAngle else (1 if enemy['angle'] > 0 else -1)
        agentHost.sendCommand("turn {}".format(turnSpd))
        agentHost.sendCommand("move {}".format(1 if enemy['dist'] > moveDist else 0))
        #agentHost.sendCommand("attack {}".format(int(doAttack)))
        if(doAttack):
            agentHost.sendCommand("attack 1")
            agentHost.sendCommand("attack 0")
            self.lastAttackTime = time()

