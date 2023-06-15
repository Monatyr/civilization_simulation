from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils
from utils.vec2 import Vec2

import random


class ExploreAction(Action):
    def __init__(self, agent: 'SimulationAgent') -> None:
        super().__init__(agent)
        self.__claimProgress = 5


    def areConditionsMet(self):
        return True


    def perform(self):
        agentsCell = self._agent.simulationMap.getCell(self._agent.position)
        
        isActionFinished = False

        if agentsCell.civilizationType != self._agent.civilizationType:
            isActionFinished = self.claimCell(agentsCell)
        else:
            isActionFinished = self.moveToUnclaimedCell()
        
        if isActionFinished:
            self.finishAction()
    

    def claimCell(self, cell):
        self.__claimProgress -= 1

        if self.__claimProgress <= 0:
            cell.claimTerritoryOf(self._agent.civilizationType)
            return True
        
        return False
    

    def moveToUnclaimedCell(self):
        # Get all cells around agent
        radius = Vec2(1, 1)
        allCells = self._agent.simulationMap.getArea(self._agent.position, radius)
        preferableCells = []

        # Split cells by type
        for i in range(radius.x * 2 + 1):
            for j in range(radius.x * 2 + 1):
                cellPosition = self._agent.position - radius + Vec2(i, j)
                cell = allCells[i][j]
                if cell is None:
                    continue

                if cellPosition == self._agent.position or cell.civilizationType == self._agent.civilizationType:
                    continue
                else:
                    preferableCells += [cellPosition]

        # Move agent if its possible
        if len(preferableCells) > 0:
            randomCell = random.choice(preferableCells)
            self._agent.move(randomCell - self._agent.position)
        else:
            moveVector = self.__getQuarterVector(radius)
            self._agent.move(moveVector)
        
        return True


    def __getQuarterVector(self, radius: Vec2) -> Vec2:
        if self._agent.position.x > self._agent.simulationMap.width / 2:  # II,III Quarter
            if self._agent.position.y > self._agent.simulationMap.height / 2:
                return Vec2(
                    random.randint(-radius.x, 0),  # II
                    random.randint(-radius.y, 0)
                )
            else:
                return Vec2(
                    random.randint(-radius.x, 0),  # III
                    random.randint(0, radius.y)
                )
        elif self._agent.position.x < self._agent.simulationMap.width / 2:  # I,IV Quarter
            if self._agent.position.y > self._agent.simulationMap.height / 2:
                return Vec2(
                    random.randint(0, radius.x),  # I
                    random.randint(-radius.y, 0)
                )
            else:
                return Vec2(
                    random.randint(0, radius.x),  # IV
                    random.randint(0, radius.y)
                )
        else:
            return self.__handleQuarterAxis(radius)


    def __handleQuarterAxis(self, radius: Vec2):
        if self._agent.position.x == self._agent.simulationMap.width / 2:  # Y axis split
            if self._agent.position.y > self._agent.simulationMap.height / 2:
                return Vec2(
                    0,  # I,II split
                    random.randint(-radius.y, 0)
                )
            else:
                return Vec2(
                    0,  # III,IV split
                    random.randint(0, radius.y)
                )
        elif self._agent.position.y == self._agent.simulationMap.height / 2:  # X axis split
            if self._agent.position.x > self._agent.simulationMap.height / 2:
                return Vec2(
                    random.randint(-radius.x, 0),  # II,III split
                    0
                )
            else:
                return Vec2(
                    random.randint(0, radius.x),  # I,IV split
                    0
                )
        else:
            return Vec2(0, 0)
