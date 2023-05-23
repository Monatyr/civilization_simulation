from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils
from utils.vec2 import Vec2

import random

class FightAction (Action):
    def areConditionsMet(self):
        agentsCell = self._agent.simulationMap.getCell(self._agent.position)
        self.__agentsOnCell = agentsCell.getAgents()

        isEnemyOnCell = False

        for agent in self.__agentsOnCell:
            if agent.civilizationType != self._agent.civilizationType:
                isEnemyOnCell = True
                break
        
        if not isEnemyOnCell:
            return False
        
        return True
    
    
    def perform(self):
        alliesStrength = 0
        enemiesStrength = 0

        for agent in self.__agentsOnCell:
            if agent.civilizationType == self._agent.civilizationType:
                alliesStrength += agent.attack
            else:
                enemiesStrength += agent.attack
        
        fightResult = alliesStrength - enemiesStrength + random.uniform(-3.0, 3.0)

        if fightResult < 0:
            self._agent.hurt(1)
            self.finishAction()
