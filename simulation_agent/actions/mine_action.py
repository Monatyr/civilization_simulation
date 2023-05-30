from simulation_agent.actions.action import Action


class MineAction(Action):
    def areConditionsMet(self):
        return self._agent.simulationMap.getCell(self._agent.position).resources > 0

    def perform(self):
        agentCell = self._agent.simulationMap.getCell(self._agent.position)
        agentCell.mineResource()
        self.finishAction()
