import pygame

class Case:

    def __init__(self, conf, level, case_x, case_y):

        self.case_x = case_x
        self.case_y = case_y
        self.conf = conf
        self.coord_x = self.case_x * conf.get("tile_width")
        self.coord_y = self.case_y * conf.get("tile_height")
        self.level = level
        self.is_in_boundaries = self.assert_case_is_in_level_boundaries()
        self.current_color = None
        if self.is_in_boundaries:
            self.case_type = self.get_case_type()
        else:
            self.case_type = None

    def is_same_position(self, target):

        if target.case == self:
            return True
        return False

    def is_valid(self):

        if self.is_in_boundaries and self.case_type != "1" and self.case_type is not None:
            return True
        else:
            return False

    def __eq__(self, other):

        if self.case_x == other.case_x \
                and self.case_y == other.case_y\
                and self.level == other.level:
            return True
        else:
            return False

    def __str__(self):

        return "coord_x : %s, coord_y : %s, case_x: %s, case_y: %s, case_type: %s, valid: %s" %(self.coord_x, self.coord_y, self.case_x, self.case_y, self.case_type, self.is_valid())

    def get_case_type(self):

        return self.level.level[self.case_y][self.case_x]

    def assert_case_is_in_level_boundaries(self):

        #Rules for a case to be valid
        #In the LevelGrid

        if not self.case_x <= self.level.level_grid_width - 1:
            return False

        if not self.case_x >= 0:
            return False

        if not self.case_y >= 0:
            return False

        if not self.case_y <= self.level.level_grid_height - 1:
            return False


        return True

    #def assert_case_is_not_wall(self):

    def draw_case(self, window, color):
        self.current_color = color
        pygame.draw.rect(window, color,
                         (self.coord_x, self.coord_y, self.conf.get("tile_width"), self.conf.get("tile_height")))


    def clear_case(self, window):
        pygame.draw.rect(window, self.current_color,
                         (self.coord_x, self.coord_y, self.conf.get("tile_width"), self.conf.get("tile_height")))