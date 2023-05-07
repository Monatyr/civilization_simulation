import random
import pygame

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

    def render(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.__cells[x][y]
                resources_color = (255, 255, 0) # yellow
                territory_color = None

                if cell.resources > 0:
                    pygame.draw.rect(surface, resources_color, (x*10, y*10, 10, 10))
                
                if cell.civilizationType == CivilizationType.RED:
                    territory_color = (255, 0, 0) # red
                elif cell.civilizationType == CivilizationType.BLUE:
                    territory_color = (0, 0, 255) # blue

                if territory_color is not None:
                    pygame.draw.rect(surface, territory_color, (x*10+2, y*10+2, 6, 6))

        # Draw grid
        for x in range(self.width+1):
            pygame.draw.line(surface, (128,128,128), (x*10, 0), (x*10, self.height*10))
        
        for y in range(self.height+1):
            pygame.draw.line(surface, (128,128,128), (0, y*10), (self.width*10, y*10))

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
