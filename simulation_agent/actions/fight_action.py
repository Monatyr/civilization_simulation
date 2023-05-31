from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils
from utils.vec2 import Vec2

import random

class FightAction (Action):
    def areConditionsMet(self):
        self.__agentsCell = self._agent.simulationMap.getCell(self._agent.position)
        return self.__agentsCell.isFight()
    
    def perform(self):
        alliesStrength = 0
        enemiesStrength = 0

        agentsOnCell = self.__agentsCell.getAgents()
        for agent in agentsOnCell:
            if agent.civilizationType == self._agent.civilizationType:
                alliesStrength += agent.attack
            else:
                enemiesStrength += agent.attack
        
        fightResult = alliesStrength - enemiesStrength + random.uniform(-3.0, 3.0)

        if fightResult < 0:
            self._agent.hurt(1)
            self.finishAction()
