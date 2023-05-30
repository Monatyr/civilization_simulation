from typing import List, Union

from simulation_agent.civilization_type import CivilizationType
from simulation_agent.simulation_agent import SimulationAgent

class Cell():
    def __init__(self):
        self.civilizationType = CivilizationType.NONE
        self.resources = 0
        self._agents = {}

        self._redAgentsAmount = 0
        self._blueAgentsAmount = 0
    
    # RESOURCES

    def getResources(self):
        return self.resources
    

    def setResources(self, amount):
        self.resources = amount


    def mineResource(self):
        if self.resources > 0:
            self.resources -= 1
            return self.resources
        
        return False

    # ------------------------------------

    # AGENTS
    def getAgents(self) -> List[SimulationAgent]:
        return list(self._agents.values())


    def addAgent(self, agent :SimulationAgent):
        self._agents[agent.id] = agent

        if agent.civilizationType == CivilizationType.RED:
            self._redAgentsAmount += 1
        else:
            self._blueAgentsAmount += 1
    
    
    def removeAgent(self, agentID :Union[int, SimulationAgent]) -> bool:
        if isinstance(agentID, SimulationAgent):
            agentID = agentID.id
        
        if agentID in self._agents:
            agent = self._agents[agentID]
            
            if agent.civilizationType == CivilizationType.RED:
                self._redAgentsAmount -= 1
            else:
                self._blueAgentsAmount -= 1
            
            del self._agents[agentID]
            return True
        else:
            return False
        
    # ------------------------------------

    def claimTerritoryOf(self, civilizationType :CivilizationType):
        self.civilizationType = civilizationType

    # ------------------------------------

    def isFight(self):
        return self._redAgentsAmount > 0 and self._blueAgentsAmount > 0
    