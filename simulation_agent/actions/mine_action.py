from simulation_agent.actions.action import Action
from numpy import concatenate
from utils.vec2 import Vec2

class MineAction(Action):
    def __init__(self, agent :'SimulationAgent') -> None:
        super().__init__(agent)
        self.counter = 0
        self.is_on_resources = False
        self.closest = None


    def areConditionsMet(self):
        if self._agent.simulationMap.getCell(self._agent.position).resources > 0:
            self.is_on_resources = True
            return True
        
        self.is_on_resources = False

        surroundings = self._agent.simulationMap.getArea(self._agent.position, Vec2(4, 4))
        surroundings = list(concatenate(surroundings).flat)
        surroundings = list(filter(lambda x: x is not None, surroundings))
        resources = list(filter(lambda x: x.resources > 0, surroundings))

        if not resources:
            return False
        
        self.closest = min(resources, key=lambda x: x.pos.distance(self._agent.position))
        return True


    def perform(self):
        # go in direction of the closest resource cell
        if not self.is_on_resources:
            move_vector = (self.closest.pos - self._agent.position).to_unit()
            self._agent.move(move_vector)
        else:
            healthRestoredScale = 0.2
            agentCell = self._agent.simulationMap.getCell(self._agent.position)
            agentCell.mineResource()
            self._agent.heal(healthRestoredScale)
        
        self.counter += 1
        if self.counter == 5:
            self.finishAction()
