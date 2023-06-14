from __future__ import annotations
import random
import pygame
from typing import List

from simulation_agent.civilization_type import CivilizationType
from simulation_agent.actions.help_action import HelpAction
from simulation_agent.actions.run_action import RunAction
from simulation_agent.actions.fight_action import FightAction
from simulation_agent.actions.explore_action import ExploreAction
from simulation_agent.actions.train_action import TrainAction
from simulation_agent.actions.action_type import ActionType
from simulation_agent.actions.reproduction_action import ReproductionAction
from simulation_agent.actions.mine_action import MineAction
from utils.vec2 import Vec2


class SimulationAgent:
    __id_counter = 0
    __sight = 5
    __max_health = 100

    def __init__(
            self,
            simulationMap: 'SimulationMap',
            civilizationType: CivilizationType,
            position: Vec2,
            health: int = 100,
            attack: int = 0.1,
            regeneration: float = None,
            actionVector: list[ActionType] = None
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
        self.actionVector = actionVector

        if self.actionVector is None:
            self.actionVector = ActionType.getStandardActions()

            for _ in range(32 - len(self.actionVector)):
                self.actionVector.append(random.choice(ActionType.getStandardActions()))

        if self.regeneration is None:
            self.regeneration = random.uniform(0.05, 0.1)

        # Ensure values are between correct ranges

        if self.health > SimulationAgent.__max_health:
            self.health = SimulationAgent.__max_health

        if self.health <= 0:
            self.health = 1

        if self.regeneration < 0.05:
            self.regeneration = 0.05

        if self.regeneration > 0.1:
            self.regeneration = 0.1

        # add to cell
        self.simulationMap.getCell(self.position).addAgent(self, True)

    # RENDER

    def render(self, surface, viewPos: Vec2):
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
        # check priority actions
        selectedPrimaryAction = self._selectPrimaryAction()

        if selectedPrimaryAction is not None:
            self.currentAction = self._instantiateActionFromType(
                selectedPrimaryAction
            )

        # do normal actions
        if self.currentAction is None or self.currentAction.is_finished():
            self.currentAction = self._instantiateActionFromType(
                self._selectNewAction()
            )

        # check conditions (if conditions for the action not met - choose a new one)
        tries = 0

        while not self.currentAction.areConditionsMet():
            self.currentAction = self._instantiateActionFromType(
                self._selectNewAction()
            )

            tries += 1

            if tries > 100:
                break

        # perform action
        self._doAction()

    # TODO: maybe create action only once and repurpose it? Should help with optimization
    def _instantiateActionFromType(self, actionType):
        if actionType == ActionType.HELP:
            return HelpAction(self)
        elif actionType == ActionType.RUN_AWAY:
            return RunAction(self)
        elif actionType == ActionType.FIGHT:
            return FightAction(self)
        elif actionType == ActionType.TRAIN:
            return TrainAction(self)
        elif actionType == ActionType.BREED:
            return ReproductionAction(self)
        elif actionType == ActionType.MINE:
            return MineAction(self)
        else:
            return ExploreAction(self)

    def _selectPrimaryAction(self):
        if RunAction(self).areConditionsMet():
            return ActionType.RUN_AWAY

        if FightAction(self).areConditionsMet():
            return ActionType.FIGHT

        if HelpAction(self).areConditionsMet():
            return ActionType.HELP

        return None

    def _selectNewAction(self):
        return self.actionVector[
            random.randrange(0, len(self.actionVector))
        ]

    def _doAction(self):
        action = self.currentAction

        if action is None:
            return

        action.perform()

    # --------------------------------------------

    def getSeenSimulationMapArea(self) -> List[List["Cell"]]:
        return self.simulationMap.getArea(self.position, Vec2(SimulationAgent.__sight, SimulationAgent.__sight))

    def move(self, moveVector):
        oldPosition = self.position

        self.position += moveVector
        newCell = self.simulationMap.getCell(self.position)

        moved = False

        if newCell is not None:
            # if move succedeed
            # move agent into it
            moved = newCell.addAgent(self)

        if moved:
            self.simulationMap.getCell(oldPosition).removeAgent(self)
        else:
            # if not (eg. case: tried to move outside the map or cell is crouded)
            # move back
            self.position = oldPosition

    def die(self):
        self.simulationMap.getCell(self.position).removeAgent(self)

    def hurt(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.die()

    def heal(self, amount):
        self.health = self.__max_health if self.health + amount > self.__max_health else self.health + amount

    def reproduce(self, other: SimulationAgent):
        v1, v2 = self.actionVector, other.actionVector
        n = len(v1)
        new_v = v1[:n // 4] + v2[n // 4: n // 2] + v1[n // 2: 3 * (n // 4)] + v2[n // 4:]
        new_v = random.shuffle(self.fillActionVector(new_v))

        a1, a2 = self.attack, other.attack
        new_a = round((a1 + a2) / 2, 2)

        # TOD: regeneration
        new_agent = SimulationAgent(self.simulationMap, self.civilizationType,
                                    self.position.getNewV(), self.__max_health // 2, new_a, None, new_v)

        # lower the health of both parents
        self.health = self.health // 2
        other.health = other.health // 2

    # might be unneccessary and slow down the performance
    def fillActionVector(self, vector):
        '''Ensure that action vector has at least one action of every type'''
        actions = ActionType.getStandardActions()
        actions_count = {}
        res = []

        for a in vector:
            actions_count[a] = actions_count.get(a, 0) + 1

        to_fill, to_draw_from = [], []
        for a in actions:
            if actions_count.get(a, 0) == 0:
                to_fill.append(a)
            elif actions_count.get(a) > 1:
                to_draw_from.append(a)

        for a in to_fill:
            res.append(a)
            drawn_a = random.choice(to_draw_from)
            actions_count[drawn_a] -= 1
            if actions_count[drawn_a] < 2:
                to_draw_from.remove(drawn_a)

        for a in to_draw_from:
            res.extend([a for _ in range(actions_count[a])])

        return res
    
    def __str__(self):
        return f"Pos: {self.position}, Civ: {self.civilizationType.name}, Health: {self.health}, Attack: {self.attack}, Action: {self.currentAction}, ID: {self.id}"
