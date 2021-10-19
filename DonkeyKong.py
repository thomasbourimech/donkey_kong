import pygame
from pygame.locals import *
from common.GenericLib import GenericLib
from common.GameEngine import GameEngine
import logging

logger = logging.getLogger("DonkeyKong")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
conf = GenericLib.load_json_conf("ressources/dk.json")


start = pygame.time.get_ticks()
GameEngine = GameEngine()
GameEngine.run(conf, "level_2")


