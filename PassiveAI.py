from AI import AI

class PassiveAI(AI):
    def run(self, agentHost):
        turnAngle = 80      # Angle at which agent will turn at full speed. If set too low, agent will oscillate
        enemy = self.opponents[0]
        self.turning = enemy['angle'] / turnAngle if abs(enemy['angle']) < turnAngle else (1 if enemy['angle'] > 0 else -1)
        agentHost.sendCommand("turn {}".format(self.turning))
