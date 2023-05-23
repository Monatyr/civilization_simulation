from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils
from utils.vec2 import Vec2

import random

class RunAction (Action):
    def areConditionsMet(self):
        if self._agent.health >= 0.1 * 100:
            return False
        
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
        
        if alliesStrength != 0:
            escapeProb = 1.5 - enemiesStrength / alliesStrength
        else:
            escapeProb = 0

        if escapeProb < 0:
            escapeProb = 0
        elif escapeProb > 1:
            escapeProb = 1
        
        if random.random() > escapeProb:
            # Run action failed
            self.finishAction()
            return

        # Run away
        moveVector = Vec2(
            random.randint(-1, 1),
            random.randint(-1, 1)
        )

        if moveVector.x == 0 and moveVector.y == 0:
            moveVector.y = 1
        
        self._agent.move(moveVector)

        self.finishAction()
