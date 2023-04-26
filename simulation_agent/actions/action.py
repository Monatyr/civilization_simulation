from simulation_agent.actions.action_type import ActionType
from simulation_agent.simulation_agent import SimulationAgent

class Action:
    def __init__(self, agent :SimulationAgent) -> None:
        self._agent = agent
        self._map = agent.getSeenSimulationMapArea()
        self.__finished = False

    def finishAction(self):
        self.__finished = True

    def areConditionsMet(self):
        return True

    def perform(self):
        pass
