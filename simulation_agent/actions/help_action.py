from functools import reduce
import math

from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils



class HelpAction (Action):
    def __getAgentsThatAreCallingHelp(self):
        return CellUtils.map_cells(
            self._map,
            lambda cell: list(filter(
                lambda agent: agent.isCallingForHelp(),
                cell.getAgents()
            ))
        )
    
    def areConditionsMet(self):
        agentsThatAreCallingHelp = self.__getAgentsThatAreCallingHelp()
        return len(agentsThatAreCallingHelp) > 0
    
    def perform(self):
        agentsThatAreCallingHelp = self.__getAgentsThatAreCallingHelp()

        closestAgent = reduce(
            lambda min, current: current if current[0] < min[0] else min,
            map(
                lambda agent: [
                    (agent.position - self._agent.position).length(),
                    agent
                ],
                agentsThatAreCallingHelp
            ),
            [999999999, None]
        )[1]

        moveVector = closestAgent.position - self._agent.position
        
        moveVector.normalized()

        if moveVector.x > 0.5:
            moveVector.x = 1
        
        if moveVector.x < -0.5:
            moveVector.x = -1

        if moveVector.y > 0.5:
            moveVector.y = 1
        
        if moveVector.y < -0.5:
            moveVector.y = -1
        
        self._agent.move(moveVector)

        if self._agent.position == closestAgent.position or moveVector.isZero():
            self.finishAction()
