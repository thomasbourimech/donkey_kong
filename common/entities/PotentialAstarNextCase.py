from common.Case import Case
import pygame
class PotentialAstarNextCase(Case):

    def __init__(self, conf, level, case_x, case_y, g, h, f, parent_case):
        super().__init__(conf, level, case_x, case_y)
        self.conf = conf
        self.distance = None
        self.nb_visit = 0
        if parent_case is not None:
            self.parent_case = parent_case
        else:
            self.parent_case = None
        self.g = g
        self.h = h
        self.f = f

    def count_nb_of_visite_for_case(self, pathfinder_cases_visited):

        count = 0
        for case in pathfinder_cases_visited:

            if case == self:
                count += 1

        return count

    def __str__(self):
        if self.parent_case is not None:
            return super().__str__() + ", d=" + str(self.distance) + ", visited=" + str(self.nb_visit) + ", g:" \
                   + str(self.g) + ", h:" + str(self.h) + ", f:" + str(self.f) + ", parent_x:" + str(self.parent_case.case_x) + ", parent_y:" + str(self.parent_case.case_y)
        else:
            return super().__str__() + ", d=" + str(self.distance) + ", visited=" + str(self.nb_visit) + ", g:" \
                   + str(self.g) + ", h:" + str(self.h) + ", f:" + str(self.f) + ", parent_x: None, parent_y: None"

    def draw_case(self, window, color):

        super().draw_case(window, color)
        self.write_info_in_case(window)

    def write_info_in_case(self, window):

        self.clear_case(window)

        font = pygame.font.Font(None, 15)
        g = font.render("g:%s" % '{0:.3g}'.format(self.g), 1, (255, 255, 255))
        h = font.render("h:%s" % '{0:.3g}'.format(self.h), 1, (255, 255, 255))
        f = font.render("f:%s" % '{0:.3g}'.format(self.f), 1, (255, 255, 255))
        window.blit(g, (self.coord_x, self.coord_y))
        window.blit(h, (self.coord_x, self.coord_y + 10))
        window.blit(f, (self.coord_x, self.coord_y + 20))

        case_x = font.render("x:%s" % self.case_x, 1, (255, 255, 255))
        case_y = font.render("y:%s" % self.case_y, 1, (255, 255, 255))
        window.blit(case_x, (self.coord_x+ 30, self.coord_y))
        window.blit(case_y, (self.coord_x + 30, self.coord_y + 10))

        if self.parent_case is not None:
            p_case_x = font.render("px:%s" % self.parent_case.case_x, 1, (255, 255, 255))
            p_case_y = font.render("py:%s" % self.parent_case.case_y, 1, (255, 255, 255))
            window.blit(p_case_x, (self.coord_x + 30, self.coord_y + 20))
            window.blit(p_case_y, (self.coord_x + 30, self.coord_y + 30))
