import pygame

class Engine():
    def __init__(self, config):
        self.config = config

        self.running = True
    
    def run(self):
        while self.running:
            self.run_loop()


    def run_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            