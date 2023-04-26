import random
from typing import List

from simulation_agent.civilization_type import CivilizationType
from simulation_agent.actions.action import Action
from simulation_agent.actions.help_action import HelpAction
from simulation_agent.actions.run_action import RunAction
from simulation_agent.actions.action_type import ActionType
from simulation_map.simulation_map import SimulationMap
from utils.vec2 import Vec2

class SimulationAgent():
    __id_counter = 0
    __sight = 5
    __max_health = 100

    def __init__(
        self,
        simulationMap: SimulationMap,
        civilizationType :CivilizationType,
        position :Vec2,
        health :int = 100,
        attack :int = 0.0,
        regeneration :float = None
    ):
        self.id = SimulationAgent.__id_counter
        SimulationAgent.__id_counter += 1

        self.simulationMap = simulationMap

        self.civilizationType = civilizationType
        self.position = position
        self.isCallingForHelp = False

        self.health = health
        self.attack = attack
        self.regeneration = regeneration

        self.currentAction = None
        self.actionVector = []

        for at in ActionType.getStandardAcitons():
            self.actionVector += [at]

        for i in range(32 - len(self.actionVector)):
            self.actionVector += [
                random.choice(ActionType.getStandardAcitons())
            ]

        if self.regeneration is None:
            self.regeneration = random.uniform(0.05, 0.1)
        
        # Ensure values are between correct ranges
        
        if self.health > SimulationAgent.__max_health:
            self.health = SimulationAgent.__max_health
        
        if self.health < 0:
            self.health = 0
        
        if self.regeneration < 0.05:
            self.regeneration = 0.05

        if self.regeneration > 0.1:
            self.regeneration = 0.1

    # ACTIONS

    def act(self):
        if self.currentAction == None:
            self.currentAction = Action(
                self._selectNewAction()
            )
        
        self._doAction()
    
    def _selectNewAction(self):
        # check priority actions

        if HelpAction(self).areConditionsMet():
            return ActionType.HELP

        if RunAction(self).areConditionsMet():
            return ActionType.RUN_AWAY

        return self.actionVector[
            random.randrange(0, len(self.actionVector))
        ]

    def _doAction(self):
        action = self.currentAction
        action.perform()
    
    # --------------------------------------------

    def getSeenSimulationMapArea(self) -> List[List["Cell"]]:
        return self.simulationMap.getArea(self.position, Vec2(SimulationAgent.__sight, SimulationAgent.__sight))

    def move(self, moveVector):
        self.simulationMap.getCell(self.position).removeAgent(self)
        self.position += moveVector
        self.simulationMap.getCell(self.position).addAgent(self)
