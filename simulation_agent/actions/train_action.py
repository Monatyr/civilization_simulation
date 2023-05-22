from simulation_agent.actions.action import Action


class TrainAction(Action):
    def areConditionsMet(self):
        return super().areConditionsMet()
    

    def perform(self):
        self._agent.attack += 20 / (self._agent.attack + 10)
        self._agent.attack = round(self._agent.attack, 2)
        self.finishAction()