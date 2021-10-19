from common.Character import Character
from common.PathFinder import PathFinder
from common.PathFinderAstar import PathFinderAstar
from common.PathFinderService import PathFinderService
from common.Case import Case
import random
import pygame


class Baddie(Character):

    def __init__(self, conf, x, y, level, target, path_finder_type="astar"):

        super().__init__(conf, level)
        self.conf = conf
        self.case = Case(self.conf, level, x, y)
        self.next_case = Case(self.conf, level, 0, 0)
        self.sprite = None
        self.level = level
        self.sprite = "dk_down"
        self.type = self.type + "::" + self.__class__.__name__
        self.target = target
        if path_finder_type == "mine":
            self.path_finder = PathFinder(conf, level, self)
        else:
            self.path_finder = PathFinderService(conf, level)


    def move_right(self):

        self.sprite = "dk_right"
        super().move_right()

    def move_left(self):

        self.sprite = "dk_left"
        super().move_left()

    def move_up(self):

        self.sprite = "dk_up"
        super().move_up()


    def move_down(self):

        self.sprite = "dk_down"
        super().move_down()


    def display(self, window, pygame_ressources):

        x = self.case.case_x * self.conf.get("sprite_width")
        y = self.case.case_y * self.conf.get("sprite_height")

        window.blit(pygame_ressources[self.sprite], (x, y))


    def auto_move_random(self):

        movement = random.randrange(0, 4)

        if movement == 0:
            self.move_up()
        elif movement == 1:
            self.move_right()
        elif movement == 2:
            self.move_down()
        elif movement == 3:
            self.move_left()
        clock = pygame.time.Clock()



    def auto_move_with_pathfinder(self):

        self.move_to_case(self.path_finder.compute_next_position())

    def get_path_to_target(self):

        self.path_finder.compute_next_position()



    def draw_case(self, conf, window, case, color):

        case.draw_case(conf, window, color, (case.coord_x, case.coord_y, self.conf.get("sprite_width"), self.conf.get("sprite_height")))

