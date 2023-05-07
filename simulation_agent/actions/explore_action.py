from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils
from utils.vec2 import Vec2

import random

class ExploreAction (Action):
    def areConditionsMet(self):
        return True
    
    def perform(self):
        # TODO: make movement not random
        moveVector = Vec2(
            random.randint(-1, 1),
            random.randint(-1, 1)
        )

        if moveVector.x == 0 and moveVector.y == 0:
            moveVector.y = 1
        
        self._agent.move(moveVector)

        self.finishAction()
