from enum import Enum

class ActionType (Enum):
    HELP = -1
    RUN_AWAY = -2
    FIGHT = -3
    
    GO_FIGHT = 1
    CALL_HELP = 2
    EXPLORE = 3
    MINE = 4
    BREED = 5
    TRAIN = 6


    def getPriorityActions():
        return [
            ActionType.HELP,
            ActionType.RUN_AWAY,
            ActionType.FIGHT,
        ]


    def getStandardAcitons():
        return [
            ActionType.GO_FIGHT,
            ActionType.CALL_HELP,
            ActionType.EXPLORE,
            ActionType.MINE,
            ActionType.BREED,
            ActionType.TRAIN,
        ]
