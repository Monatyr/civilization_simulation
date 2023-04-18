import pygame
import json
from engine import Engine

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((400, 500))
    pygame.display.set_caption('Civilisation Evolution')

    with open('config.json') as file:
        config = json.load(file)

    engine = Engine(config)
    engine.run()