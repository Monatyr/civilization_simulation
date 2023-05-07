from simulation_agent.actions.action import Action
from simulation_map.cell.cell_utils import CellUtils

class RunAction (Action):
    def areConditionsMet(self):
        # TODO: this condition has changed - update it
        if self._agent.health >= 0.1 * 100:
            return False
        
        agentsCell = self._agent.simulationMap.getCell(self._agent.position)
        agentsOnCell = agentsCell.getAgents()

        isEnemyOnCell = False

        for agent in agentsOnCell:
            if agent.civilizationType != self._agent.civilizationType:
                isEnemyOnCell = True
                break
        
        if not isEnemyOnCell:
            return False
        
        return True
    
    def perform(self):
        pass
