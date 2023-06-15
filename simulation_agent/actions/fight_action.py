from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils
from utils.vec2 import Vec2
import random


class FightAction (Action):
    def __init__(self, agent: "SimulationAgent"):
        super().__init__(agent)
        self._agent.alreadyFought = False
        self._agent.isCallingForHelp = False


    def areConditionsMet(self):
        self.__agentsCell = self._agent.simulationMap.getCell(self._agent.position)
        return self.__agentsCell.isFight()
    

    def perform(self):
        if self._agent.alreadyFought:
            self.finishAction()
            return

        agentsOnCell = self.__agentsCell.getAgents()
        allies = list(filter(lambda x: x.civilizationType == self._agent.civilizationType, agentsOnCell))
        enemies = list(filter(lambda x: x.civilizationType != self._agent.civilizationType, agentsOnCell))

        alliesStrength = sum(list(map(lambda x: x.attack, allies)))
        enemiesStrength = sum(list(map(lambda x: x.attack, enemies)))
        random_range = 3
        fightResult = alliesStrength - enemiesStrength + random.uniform(-random_range, random_range)

        cell = self._agent.simulationMap.getCell(self._agent.position) 

        if fightResult < 0:
            for ally in allies:
                ally.hurt(1)
                ally.alreadyFought = True
                if fightResult < -random_range:
                    ally.isCallingForHelp = True
        else:
            for enemy in enemies:
                enemy.hurt(1)
                enemy.alreadyFought = True
                if fightResult > random_range:
                    enemy.isCallingForHelp = True

        self.finishAction()
