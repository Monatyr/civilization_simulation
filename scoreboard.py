from utils.vec2 import Vec2
from simulation_agent.civilization_type import CivilizationType
import utils.plots
import utils.pickle

class CivilizationScore:
    resourcesMined = {
        CivilizationType.RED: 0,
        CivilizationType.BLUE: 0,
    }

    fightsWon = {
        CivilizationType.RED: 0,
        CivilizationType.BLUE: 0,
    }

    @staticmethod
    def addResourceMined(civilizationType :CivilizationType, amount :int = 1):
        if civilizationType in CivilizationScore.resourcesMined:
            CivilizationScore.resourcesMined[civilizationType] += amount
    
    @staticmethod
    def addFightsWon(civilizationType :CivilizationType, amount :int = 1):
        if civilizationType in CivilizationScore.fightsWon:
            CivilizationScore.fightsWon[civilizationType] += amount
    
    @staticmethod
    def getResourcesMined(civilizationType :CivilizationType):
        if civilizationType not in CivilizationScore.resourcesMined:
            return None
        return CivilizationScore.resourcesMined[civilizationType]

    @staticmethod
    def getFightsWon(civilizationType :CivilizationType):
        if civilizationType not in CivilizationScore.fightsWon:
            return None
        return CivilizationScore.fightsWon[civilizationType]



class Scoreboard:
    def __init__(self, map) -> None:
        self.__map = map

        self.__allCount = 0
        self.__redCount = 0
        self.__blueCount = 0

        self.__pointsOverTime = {
            CivilizationType.RED: [],
            CivilizationType.BLUE: [],
        }
    
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
    
    def __savePoints(self, pnts):
        self.__pointsOverTime[CivilizationType.RED].append(pnts[CivilizationType.RED])
        self.__pointsOverTime[CivilizationType.BLUE].append(pnts[CivilizationType.BLUE])
    
    def getPointsOverTime(self):
        return self.__pointsOverTime

    def render(self):
        hasChanged = self.__count()
        pnts = self.calculatePoints()

        self.__savePoints(pnts)

        if hasChanged:
            print(
                "All:",
                self.__allCount,
                "\tRED:", self.__redCount,
                '(', int(self.__redStrength), '|', int(self.__redHealth), ')',
                "\tBLUE:", self.__blueCount,
                '(', int(self.__blueStrength), '|', int(self.__blueHealth), ')'
            )

            print("SCORES:\tred:", pnts[CivilizationType.RED], "\tblue:", pnts[CivilizationType.BLUE])
    
    def renderEnd(self):
        print(
            "All:",
            self.__allCount,
            "\tRED:", self.__redCount,
            '(', int(self.__redStrength), '|', int(self.__redHealth), ')',
            "\tBLUE:", self.__blueCount,
            '(', int(self.__blueStrength), '|', int(self.__blueHealth), ')'
        )

        pnts = self.calculatePoints()
        print("SCORES:\tred:", pnts[CivilizationType.RED], "\tblue:", pnts[CivilizationType.BLUE])

        if pnts[CivilizationType.RED] > pnts[CivilizationType.BLUE]:
            print("RED WON!")
        elif pnts[CivilizationType.RED] < pnts[CivilizationType.BLUE]:
            print("BLUE WON!")
        else:
            print("DRAW!")
        
        
        utils.pickle.savePickle('points_over_time.pkl', self.__pointsOverTime)
        utils.plots.renderPointsOverTime(self.__pointsOverTime)
    

    def getCounts(self):
        return {
            CivilizationType.RED: self.__redCount,
            CivilizationType.BLUE: self.__blueCount
        }

    def calculatePoints(self):
        self.__count()

        redTeritorySize = 0
        blueTeritorySize = 0

        for w in range(self.__map.width):
            for h in range(self.__map.height):
                cell = self.__map.getCell(Vec2(w, h))

                if cell.civilizationType == CivilizationType.RED:
                    redTeritorySize += 1
                elif cell.civilizationType == CivilizationType.BLUE:
                    blueTeritorySize += 1

        # print("red:",
        #     self.__redCount * 100,
        #     CivilizationScore.getResourcesMined(CivilizationType.RED),
        #     CivilizationScore.getFightsWon(CivilizationType.RED),
        #     redTeritorySize)
        # print("blue:",
        #     self.__blueCount * 100,
        #     CivilizationScore.getResourcesMined(CivilizationType.BLUE),
        #     CivilizationScore.getFightsWon(CivilizationType.BLUE),
        #     blueTeritorySize)
        
        redPoints = self.__redCount * 100 + \
            CivilizationScore.getResourcesMined(CivilizationType.RED) + \
            CivilizationScore.getFightsWon(CivilizationType.RED) + \
            redTeritorySize
        bluePoints = self.__blueCount * 100 + \
            CivilizationScore.getResourcesMined(CivilizationType.BLUE) + \
            CivilizationScore.getFightsWon(CivilizationType.BLUE) + \
            blueTeritorySize

        return {
            CivilizationType.RED: redPoints,
            CivilizationType.BLUE: bluePoints,
        }
