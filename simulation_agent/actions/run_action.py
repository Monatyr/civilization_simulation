from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils
from utils.vec2 import Vec2

import random

class RunAction (Action):
    def areConditionsMet(self):
        # TODO: this condition has changed - update it
        if self._agent.health >= 0.1 * 100:
            return False
        
        agentsCell = self._agent.simulationMap.getCell(self._agent.position)
        agentsOnCell = agentsCell.getAgents()

        isEnemyOnCell = False

        for agent in agentsOnCell:
            if agent.civilizationType != self._agent.civilizationType:
                isEnemyOnCell = True
                break
        
        if not isEnemyOnCell:
            return False
        
        return True
    
    def perform(self):
        moveVector = Vec2(
            random.randint(-1, 1),
            random.randint(-1, 1)
        )

        if moveVector.x == 0 and moveVector.y == 0:
            moveVector.y = 1
        
        self._agent.move(moveVector)

        self.finishAction()
