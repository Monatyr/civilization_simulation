import random

from simulation_map.cell.cell import Cell
from simulation_agent.civilization_type import CivilizationType
from utils.vec2 import Vec2

class SimulationMap():
    def __init__(
        self,
        width :int,
        height :int,
        numberOfResourcesCells :int,
        teamRedPos :Vec2,
        teamBluePos :Vec2
    ):
        self.width = width
        self.height = height

        self.__cells = []

        for x in range(self.width):
            self.__cells += [[]]

            for y in range(self.height):
                self.__cells[x] += [Cell()]
        
        self.__placeResources(numberOfResourcesCells)
        self.__placeTerritories(teamRedPos, teamBluePos)
    
    def __placeResources(self, numberOfResourcesCells):
        cellsWithResources = []

        for i in range(numberOfResourcesCells):
            randomPlace = random.randint(0, self.width * self.height - 1)
            
            if randomPlace in cellsWithResources:
                randomPlace = random.randint(0, self.width * self.height - 1)

            cellsWithResources += [randomPlace]
        
        for pos in cellsWithResources:
            x = pos % self.width
            y = int(pos / self.width)

            self.__cells[x][y].setResources(random.randint(25, 100))
    
    def __placeTerritories(self, teamRedPos :Vec2, teamBluePos :Vec2):
        self.getCell(teamRedPos).claimTerritoryOf(CivilizationType.RED)
        self.getCell(teamBluePos).claimTerritoryOf(CivilizationType.BLUE)

    # ==============================================================
    
    def getCell(self, pos) -> Cell:
        return self.__cells[pos.x][pos.y]

    def territoryOf(self, civilizationType :CivilizationType):
        ret = 0

        for x in range(self.width):
            for y in range(self.height):
                if self.__cells[x][y].civilizationType == civilizationType:
                    ret += 1
        
        return ret

    def getArea(self, center :Vec2, radius :Vec2):
        ret = []

        for i in range(radius.x * 2 + 1):
            ret[i] = []

            for j in range(radius.y * 2 + 1):
                ret[i][j] = self.getCell(center - radius + Vec2(i, j))

        return ret
