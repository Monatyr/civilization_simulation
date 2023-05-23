from utils.vec2 import Vec2
from simulation_agent.civilization_type import CivilizationType

class Scoreboard:
    def __init__(self, map) -> None:
        self.__map = map

        self.__allCount = 0
        self.__redCount = 0
        self.__blueCount = 0
    
    def __count(self):
        allCount = 0
        redCount = 0
        blueCount = 0
        redStrength = 0
        blueStrength = 0
        redHealth = 0
        blueHealth = 0

        # TODO: add method to map something like areAgentsPosChanged() and if not skip counting 

        allAgents = self.__map.getAllAgents()
        
        allCount += len(allAgents)

        for agent in allAgents:
            if agent.civilizationType == CivilizationType.RED:
                redCount += 1
                redStrength += agent.attack
                redHealth += agent.health
            elif agent.civilizationType == CivilizationType.BLUE:
                blueCount += 1
                blueStrength += agent.attack
                blueHealth += agent.health
        
        hasChanged = False

        if (
            allCount != self.__allCount
            or redCount != self.__redCount
            or blueCount != self.__blueCount
            or redStrength != self.__redStrength
            or blueStrength != self.__blueStrength
            or redHealth != self.__redHealth
            or blueHealth != self.__blueHealth
        ):
            hasChanged = True

        self.__allCount = allCount
        self.__redCount = redCount
        self.__blueCount = blueCount
        self.__redStrength = redStrength
        self.__blueStrength = blueStrength
        self.__redHealth = redHealth
        self.__blueHealth = blueHealth

        return hasChanged
    
    def render(self):
        hasChanged = self.__count()

        if hasChanged:
            print(
                "All:",
                self.__allCount,
                "\tRED:", self.__redCount,
                '(', int(self.__redStrength), '|', int(self.__redHealth), ')',
                "\tBLUE:", self.__blueCount,
                '(', int(self.__blueStrength), '|', int(self.__blueHealth), ')'
            )
