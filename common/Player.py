from common.Character import Character
from common.Case import Case

class Player(Character):


    def __init__(self, conf,  x, y, level):

        super().__init__(conf, level)
        self.conf = conf
        self.case = Case(self.conf, level, x, y)
        self.next_case = Case(self.conf, level, 0, 0)
        self.conf = conf
        self.level = level
        self.sprite = "dk_down"
        self.type = self.type + "::" + self.__class__.__name__



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
