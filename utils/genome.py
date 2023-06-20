from simulation_agent.actions.action_type import ActionType
import math
import random

class Genome:
    def __init__(self, length: int) -> None:
        self.length: int = length
        self.actions: list[ActionType] = ActionType.getStandardActions()
    
    def generate_vector(self, preferences: dict[str,float]) -> list[ActionType]:
        preferences_ints = list(map(lambda x: int(x * 1000), preferences.values()))
        assert sum(preferences_ints) == 1000, "Sum of preferences not equal to 1"
        preferences = self.__validate_preferences(preferences)

        action_vector: list[ActionType] = []
        for action in self.actions:
            vector_size = int(math.ceil(self.length * preferences[action.name.lower()]))
            specialized_vector = [action]*vector_size
            action_vector += specialized_vector
        
        return self.adjust_vector(action_vector)

    def __validate_preferences(self, preferences: dict[str,float]) -> dict[str,float]:
        if len(preferences.keys()) != len(self.actions):
            return self.__generate_preferences()
        else:
            return preferences
        

    def __generate_preferences(self) -> dict[str,float]:
        ratio: float = math.ceil(1.0 / len(self.actions))
        fresh_preferences = {}
        for action in self.actions:
            fresh_preferences[action.name.lower()] = ratio
        
        return fresh_preferences

    def create_crossbred_vector(self, first_vector: list[ActionType], second_vector: list[ActionType], mutation_prob: float) -> list[ActionType]:
        first_quarter: int = self.length//4
        second_quarter: int = first_quarter*2
        third_quarter: int = first_quarter*3

        new_vector: list[ActionType] = []
        new_vector += first_vector[:first_quarter] + first_vector[second_quarter:third_quarter]
        new_vector += second_vector[first_quarter:second_quarter] + second_vector[third_quarter:]

        new_vector = self.adjust_vector(new_vector)
        if random.random() < mutation_prob:
            for _ in range(4):
                new_vector[random.randint(0,31)] = random.choice(self.actions)
        
        return sorted(new_vector)

    def adjust_vector(self, action_vector: list[ActionType]) -> list[ActionType]:
        random.shuffle(action_vector)
        valid_vector = action_vector[:self.length]
        return sorted(valid_vector)