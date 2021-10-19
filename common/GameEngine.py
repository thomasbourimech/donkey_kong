from common.LevelProcessor import levelGrid
from common.entities.CasesList import CasesList
from common.PathFinderService import PathFinderService
from common.Player import Player
from common.Baddie import Baddie
import pygame

import logging

from pygame.locals import *
logger = logging.getLogger("DonkeyKong")

class GameEngine:

    def run(self, conf, level):
        conf.get("level_path")
        level = levelGrid(conf.get("level_path") + "/" + level + ".txt")
        player = Player(conf, 0, 0, level)
        baddie = Baddie(conf, 14, 14, level, target=player, path_finder_type="astar")


        nb_tile_width = level.level_grid_width
        nb_tile_height = level.level_grid_height
        sprite_width = conf.get("sprite_width")
        sprite_height = conf.get("sprite_height")

        window = pygame.display.set_mode((nb_tile_width * int(sprite_width),
                                          nb_tile_height * int(sprite_height)), RESIZABLE)
        pygame.time.Clock().tick(1)
        pygame_ressources = self.load_ressources(conf)
        clock = pygame.time.Clock()
        cont = True
        pygame.init()
        start = pygame.time.get_ticks()

        pause = False
        pathfinder = PathFinderService(conf, level)


        i=0
        while cont:
            logger.info("Iteration %s" %i)
            while pause:
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        if event.key == K_p:
                            pause = False

            window.fill(0)  # efface la fenetre
            self.display_level(conf, window, pygame_ressources, level)
            cont, pause = self.event_handler(player, pause)

            player.display(window, pygame_ressources)
            baddie.display(window, pygame_ressources)

            if baddie.case == player.case:
                cont = False

            closed_list, opened_list, path_finder_current_case, found_path = pathfinder.compute_full_path(baddie,
                                                                                                          player)


            #closed_list.draw_list_case(window, (255, 0, 0))
            #opened_list.draw_list_case(window, (0, 255, 0))
            if found_path is not None:
                 found_path.draw_list_case(window, (0, 0, 127))


                 #print("path = %s" %found_path)


            #path_finder_current_case.draw_case(window, (0, 0, 255))
            baddie.display(window, pygame_ressources)


            baddie.auto_move_random()





            #
            #baddie.auto_move_with_pathfinder(player)
            # #baddie.get_path_to_target(player)²
            # #baddie.auto_move_with_pathfinder(player)
            #baddie.auto_move_random()

            pygame.display.update()
            clock.tick(60)
            i += 1





        logger.info((str(pygame.time.get_ticks() - start) + " milliseconds"))


    def intersect(self, a, b):
        c = [val for val in b if not val in a]
        return c

    def event_handler(self, player, pause):
        cont = True
        for event in pygame.event.get():

            if event.type == KEYUP:
                if event.key == K_p:
                    pause = True

            if event.type == QUIT:
                cont = False

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    player.move_down()
                if event.key == K_UP:
                    player.move_up()
                if event.key == K_RIGHT:
                    player.move_right()
                if event.key == K_LEFT:
                    player.move_left()

        return cont, pause


    def display_level(self, conf, window, pygame_ressources, level):

        sprite_width = conf.get("sprite_width")
        sprite_height = conf.get("sprite_height")

        #window.blit(pygame_ressources["bkg"], (0, 0))
        num_line = 0
        for line in level.level:
            num_case = 0
            for sprite in line:
                x = num_case * int(sprite_width)
                y = num_line * int(sprite_height)

                if sprite == "1":
                    window.blit(pygame_ressources["wall"], (x, y))
                elif sprite == "A":
                    window.blit(pygame_ressources["start"], (x, y))
                elif sprite == "B":
                    window.blit(pygame_ressources["finish"], (x, y))
                num_case += 1
            num_line += 1

    def load_ressources(self, conf):

        ressources_path = conf.get("ressources_path")
        ressources = conf.get("ressources")
        pygame_ressources = {}
        for ressource in ressources:
            ressource_conf = ressources.get(ressource)
            ressource_filename = ressource_conf['filename']
            if ressource_conf.get("alpha"):
                pygame_ressources[ressource] = pygame.image.load(ressources_path + "/" + ressource_filename).convert_alpha()
                pygame_ressources[ressource] = pygame.transform.scale2x(pygame_ressources[ressource])
            else:
                pygame_ressources[ressource] = pygame.image.load(ressources_path + "/" + ressource_filename).convert()
                pygame_ressources[ressource] = pygame.transform.scale2x(pygame_ressources[ressource])


        return pygame_ressources