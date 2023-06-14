from simulation_agent.actions.action_type import ActionType

class Action:
    def __init__(self, agent :'SimulationAgent') -> None:
        self._agent = agent
        self._map = agent.getSeenSimulationMapArea()
        self.__finished = False


    def finishAction(self):
        self.__finished = True

    
    def is_finished(self):
        return self.__finished


    def areConditionsMet(self):
        return True


    def perform(self):
        pass


    def __str__(self) -> str:
        return self.__class__.__name__
