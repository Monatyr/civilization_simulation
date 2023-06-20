import pygame

from simulation_map.simulation_map import SimulationMap
from utils.vec2 import Vec2
from utils.genome import Genome
from simulation_agent.simulation_agent import SimulationAgent
from simulation_agent.civilization_type import CivilizationType
from scoreboard import Scoreboard

class Engine():
    def __init__(self, config, screen):
        self.config = config
        self.__screen = screen

        self.running = True
        self.paused = False

        self.view_pos = Vec2(0, 0)
        self.view_width = 20
        self.view_height = 15
        self.cell_size = 32
        self.mouse_pos = Vec2(0, 0)
        self.dragging = False

        self.prepare()
    

    def prepare(self):
        self.__map = SimulationMap(
            self.config['map']['width'], self.config['map']['height'],
            self.config['map']['numberOfResourcesCells'],
            Vec2.fromList(self.config['map']['agents']['red']['start']),
            Vec2.fromList(self.config['map']['agents']['blue']['start']),
            self.config['map']['agents']['maxAgentsOnCell'],
            self.config['genome']['mutation_prob']
        )
        self.__scoreboard = Scoreboard(self.__map)
        
        for i in range(self.config['map']['agents']['red']['population']):
            preferences = self.config['genome']['preferences']['red'] if 'red' in self.config['genome']['preferences'] else {}
            new_agent = SimulationAgent(
                self.__map,
                CivilizationType.RED,
                Vec2.fromList(self.config['map']['agents']['red']['start']),
                Genome(32).generate_vector(preferences)
            )
            self.__map.getCell(new_agent.position).addAgent(new_agent, True)
        
        for i in range(self.config['map']['agents']['blue']['population']):
            preferences = self.config['genome']['preferences']['blue'] if 'blue' in self.config['genome']['preferences'] else {}
            new_agent = SimulationAgent(
                self.__map,
                CivilizationType.BLUE,
                Vec2.fromList(self.config['map']['agents']['blue']['start']),
                Genome(32).generate_vector(preferences)
            )
            self.__map.getCell(new_agent.position).addAgent(new_agent, True)

    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused:
                self.run_loop()
        
        self.__scoreboard.renderEnd()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
                if event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    pos = Vec2(x // 10, y // 10)
                    agents = self.__map.getCell(pos).getAgents()
                    for agent in agents:
                        print(agent)
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

        # Sould end
        if self.shouldEnd():
            self.running = False
    

    def update(self):
        for agent in self.__map.getAllAgents():
            agent.act()


    def render(self):
        self.__map.render(self.__screen, self.view_pos)

        for agent in self.__map.getAllAgents():
            agent.render(self.__screen, self.view_pos)
        
        self.__scoreboard.render()
    
    def shouldEnd(self):
        populationsCounts = self.__scoreboard.getCounts()

        # end if one population is 0
        if populationsCounts[CivilizationType.RED] == 0 or populationsCounts[CivilizationType.BLUE] == 0:
            return True
        
        # end if none resources are found
        for w in range(self.__map.width):
            for h in range(self.__map.height):
                cell = self.__map.getCell(Vec2(w, h))

                if cell.resources > 0:
                    return False
        return True
