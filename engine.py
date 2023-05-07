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

        self.view_pos = Vec2(0, 0)
        self.view_width = 20
        self.view_height = 15
        self.cell_size = 32
        self.mouse_pos = Vec2(0, 0)
        self.dragging = False

        self.prepare()
    
    def prepare(self):
        self.__map = SimulationMap(100, 100, 10, Vec2(10, 10), Vec2(90, 90))
        
        self.__agents = []

        for i in range(1000):
            self.__agents += [SimulationAgent(self.__map, CivilizationType.BLUE, Vec2(10, 10))]
        
        for i in range(1000):
            self.__agents += [SimulationAgent(self.__map, CivilizationType.RED, Vec2(90, 90))]

    
    def run(self):
        while self.running:
            self.handle_events()
            self.run_loop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    delta = Vec2(event.rel[0], event.rel[1])
                    self.view_pos -= delta

                    if self.view_pos.x < 0:
                        self.view_pos.x = 0
                    
                    if self.view_pos.y < 0:
                        self.view_pos.y = 0

        self.mouse_pos = Vec2(*pygame.mouse.get_pos())
    
    def run_loop(self):
        # Clear the screen
        self.__screen.fill((255,255,255))

        # Update state
        self.update()

        # Render
        self.render()
        

        # Update the screen
        pygame.display.flip()
    
    def update(self):
        for agent in self.__agents:
            agent.act()

    def render(self):
        self.__map.render(self.__screen, self.view_pos)

        for agent in self.__agents:
            agent.render(self.__screen, self.view_pos)
