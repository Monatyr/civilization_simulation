from simulation_agent.actions.action import Action


class MineAction(Action):
    def areConditionsMet(self):
        return self._agent.simulationMap.getCell(self._agent.position).resources > 0

    def perform(self):
        healthRestoredScale = 2.0
        agentCell = self._agent.simulationMap.getCell(self._agent.position)
        mined = agentCell.mineResource()
        self._agent.heal(mined*healthRestoredScale)
        self.finishAction()
