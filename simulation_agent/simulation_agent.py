import random
import pygame
from typing import List

from simulation_agent.civilization_type import CivilizationType
from simulation_agent.actions.action import Action
from simulation_agent.actions.help_action import HelpAction
from simulation_agent.actions.run_action import RunAction
from simulation_agent.actions.explore_action import ExploreAction
from simulation_agent.actions.train_action import TrainAction
from simulation_agent.actions.action_type import ActionType
from utils.vec2 import Vec2

class SimulationAgent():
    __id_counter = 0
    __sight = 5
    __max_health = 100

    def __init__(
        self,
        simulationMap: 'SimulationMap',
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

        self.actionVector = ActionType.getStandardActions()

        for _ in range(32 - len(self.actionVector)):
            self.actionVector.append(random.choice(ActionType.getStandardActions()))

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
    
    # RENDER

    def render(self, surface, viewPos :Vec2):
        pos = self.position * 10 + Vec2(4, 4) - viewPos
        size = 6

        if pos.x < 0 or pos.y < 0 or pos.x > surface.get_width() or pos.y > surface.get_height():
            return
        
        pygame.draw.circle(
            surface,
            (50, 50, 250) if self.civilizationType == CivilizationType.BLUE else (250, 50, 50),
            (int(pos.x), int(pos.y)),
            size
        )

    # ACTIONS

    def act(self):
        if self.currentAction == None:
            self.currentAction = self._instantiateActionFromType(
                self._selectNewAction()
            )
        
        self._doAction()
    

    #TODO: implement all actions
    def _instantiateActionFromType(self, actionType):
        if actionType == ActionType.HELP:
            return HelpAction(self)
        elif actionType == ActionType.RUN_AWAY:
            return RunAction(self)
        elif actionType == ActionType.TRAIN:
            return TrainAction(self)
        else:
            return ExploreAction(self)
        
    
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
        newCell = self.simulationMap.getCell(self.position)

        if newCell is not None:
            # if move succedeed
            # move agent into it
            newCell.addAgent(self)
        else:
            # if not (eg. case: tried to move outside the map)
            # move back
            self.position -= moveVector
            self.simulationMap.getCell(self.position).addAgent(self)
