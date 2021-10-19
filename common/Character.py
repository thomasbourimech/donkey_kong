from common.Case import Case

class Character:

    def __init__(self, conf, level):
        self.conf = conf
        self.case = Case(self.conf, level, 0, 0)
        self.level = level
        self.sprite = None
        self.type = "Character"

    def __str__(self):

        return "Type: %s, %s" % (self.type, self.case)



    def move_to_potential_next_case(self, exclusion_list):

        move_to = True
        for exclusion in exclusion_list:
            if self.potential_next_case.get_case_type() == exclusion:
                move_to = False
        if move_to:
            self.case = self.potential_next_case

    def move_right(self):

        if self.case.case_x < self.level.level_grid_width - 1:
            #print("trying to go %s, %s : %s" %(self.case_x +1, self.case_y, self.level.get_case_type(self.case_x + 1, self.case_y)))
            self.potential_next_case = Case(self.conf, self.level, self.case.case_x + 1, self.case.case_y)
            self.move_to_potential_next_case(["1"])

    def move_left(self):
        if self.case.case_x > 0:
            #print("trying to go %s, %s : %s" %(self.case_x -1, self.case_y, self.level.get_case_type(self.case_x - 1, self.case_y)))
            self.potential_next_case = Case(self.conf, self.level, self.case.case_x - 1 , self.case.case_y)
            self.move_to_potential_next_case(["1"])

    def move_up(self):
        if self.case.case_y > 0:
            #print("trying to go %s, %s : %s" % (self.case_x, self.case_y - 1 , self.level.get_case_type(self.case_x, self.case_y - 1)))
            self.potential_next_case = Case(self.conf, self.level, self.case.case_x, self.case.case_y - 1)
            self.move_to_potential_next_case(["1"])

    def move_down(self):
        if self.case.case_y < self.level.level_grid_height - 1:
            #print("trying to go %s, %s : %s" % (self.case_x , self.case_y + 1 , self.level.get_case_type(self.case_x, self.case_y + 1 )))
            self.potential_next_case = Case(self.conf, self.level, self.case.case_x, self.case.case_y + 1)
            self.move_to_potential_next_case(["1"])

    def display(self, window, pygame_ressources):

        x = self.case.case_x * self.get("sprite_width")
        y = self.case.case_y * self.get("sprite_height")

        window.blit(pygame_ressources[self.sprite], (x, y))

    def move_to_case(self, case):

        self.case = case
