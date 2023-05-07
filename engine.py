import pygame

from simulation_map.simulation_map import SimulationMap
from utils.vec2 import Vec2
from simulation_agent.simulation_agent import SimulationAgent
from simulation_agent.civilization_type import CivilizationType

class Engine():
    def __init__(self, config, screen):
        self.config = config
        self.__screen = screen

        self.running = True

        self.prepare()
    
    def prepare(self):
        self.__map = SimulationMap(100, 100, 10, Vec2(10, 10), Vec2(90, 90))
        
        self.__agents = []
        self.__agents += [SimulationAgent(self.__map, CivilizationType.BLUE, Vec2(10, 10))]
        self.__agents += [SimulationAgent(self.__map, CivilizationType.RED, Vec2(90, 90))]

    
    def run(self):
        while self.running:
            self.run_loop()


    def run_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Clear the screen
        self.__screen.fill((255,255,255))

        # Render the map
        self.__map.render(self.__screen)

        # Update the screen
        pygame.display.flip()
