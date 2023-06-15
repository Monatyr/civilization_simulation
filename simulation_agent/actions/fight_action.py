from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils
from utils.vec2 import Vec2
import random


class FightAction (Action):
    def __init__(self, agent: "SimulationAgent"):
        super().__init__(agent)
        self._agent.alreadyFought = False


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
        fightResult = alliesStrength - enemiesStrength + random.uniform(-3.0, 3.0)

        cell = self._agent.simulationMap.getCell(self._agent.position) 
        print(self._agent.simulationMap.getCell(self._agent.position).isFight(), "FIGHT", self._agent.position, cell._redAgentsAmount, cell._blueAgentsAmount)

        if fightResult < 0:
            for ally in allies:
                ally.hurt(1)
                ally.alreadyFought = True
        else:
            for enemy in enemies:
                enemy.hurt(1)
                enemy.alreadyFought = True

        self.finishAction()
