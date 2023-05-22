from simulation_agent.actions.action import Action


class ReproductionAction(Action):
    def getPartner(self):
        # get agents from the same cell
        n = len(self._map)
        all_agents = self._map[n//2][n//2].getAgents()
      
        friendly_agents = list(filter(lambda x: x.civilizationType == self._agent.civilizationType, all_agents))
        friendly_agents = list(filter(lambda x: x is not self._agent, friendly_agents))
        friendly_agents = list(filter(lambda x: x.health >= 70, friendly_agents))

        if not friendly_agents:
            return None
        
        # agent with the highest health level
        partner = max(friendly_agents, key=lambda x: x.health)
        return partner


    def areConditionsMet(self):
        self.partner = self.getPartner()
        return False if self.partner is None else True
    

    def perform(self):
        self._agent.reproduce(self.partner)
        self.finishAction()


