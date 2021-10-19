from common.entities.PotentialAstarNextCase import PotentialAstarNextCase
from common.entities.CasesList import CasesList
from math import sqrt, fabs
from operator import attrgetter
import logging
logger = logging.getLogger("DonkeyKong")
MOVEMENT_COST = 10

class PathFinderService:


    def __init__(self, conf, level):

        self.iteration_nb = 0
        self.conf = conf
        self.level = level
        self.opened_list = CasesList()
        self.closed_list = CasesList()
        self.previous_target_case = None
        self.current_case = None

    def compute_full_path(self, start, target):

        found_path = None
        g = 0
        h = 0
        f = 0
        if self.current_case is None:
            self.current_case = PotentialAstarNextCase(self.conf, self.level, start.case.case_x, start.case.case_y,
                                                       g, h, f, None)
        current_case_save = self.current_case

        while not self.current_case.is_same_position(target):

            logger.info("**************NEW****************")
            logger.info("closed_list: %s " % self.closed_list)


            if self.previous_target_case is not None:
                if self.previous_target_case != target.case:
                    logger.info("Target has changed his position...Resetting pathfinder.cases_visited to []")
                    self.opened_list = CasesList()
                    self.closed_list = CasesList()
                    g = 0
                    f = 0
                    h = 0
                    self.current_case = PotentialAstarNextCase(self.conf, self.level, start.case.case_x,
                                                               start.case.case_y,
                                                           g, h, f, None)

            logger.info("target: %s : " % target)
            logger.info("current: %s : " % self.current_case)
            logger.info("continuing")

            next_case = self.compute_next_case(self.current_case, target)

            logger.info("Opened_list before pop : %s" % self.opened_list)
            self.opened_list.pop(0)
            self.closed_list.append(self.current_case)

            logger.info("Opened list after pop of lowest f : %s" % self.opened_list)
            logger.info("next_case selected for inspection = %s", next_case)

            self.current_case = next_case
            self.previous_target_case = target.case

            self.iteration_nb += 1

        if self.current_case.is_same_position(target):
            self.closed_list.append(self.current_case)
            logger.info("target: %s : " % target)
            logger.info("orig: %s : " % self.current_case)
            print("===========TARGET FOUND============")
            found_path = self.get_found_path(start, target)

        return self.closed_list, self.opened_list, current_case_save, found_path



    def compute_full_path_old(self, start, target):


        g = 0
        h = 0
        f = 0
        if self.current_case is None:
            self.current_case = PotentialAstarNextCase(self.conf, self.level, start.case.case_x, start.case.case_y,
                                                       g, h, f, None)



        found_path = None
        logger.info("**************NEW****************")
        logger.info("closed_list: %s " % self.closed_list)

        current_case_save = self.current_case

        if self.previous_target_case is not None:
            if self.previous_target_case != target.case:
                logger.info("Target has changed his position...Resetting pathfinder.cases_visited to []")
                self.opened_list = CasesList()
                self.closed_list = CasesList()
                g = 0
                f = 0
                h = 0
                self.current_case = PotentialAstarNextCase(self.conf, self.level,  start.case.case_x,
                                                      start.case.case_y,
                                                      g, h, f, None)

        if self.current_case.is_same_position(target):
            self.closed_list.append(self.current_case)
            logger.info("target: %s : " % target)
            logger.info("orig: %s : " % self.current_case)
            print("===========TARGET FOUND============")
            found_path = self.get_found_path(start, target)

        else:
            logger.info("target: %s : " % target)
            logger.info("current: %s : " % self.current_case)
            logger.info("continuing")

            next_case = self.compute_next_case(self.current_case, target)

            logger.info("Opened_list before pop : %s" % self.opened_list)
            self.opened_list.pop(0)
            self.closed_list.append(self.current_case)

            logger.info("Opened list after pop of lowest f : %s" % self.opened_list)
            logger.info("next_case selected for inspection = %s", next_case)

            self.current_case = next_case
            self.previous_target_case = target.case

        self.iteration_nb += 1

        return self.closed_list, self.opened_list, current_case_save, found_path

    def compute_next_case(self, current_case, target):

        logger.info("============New next positions sets computation initiated=============")
        logger.info("Moves originate from %s", current_case)
        self.compute_list_potential_next_case(current_case, target)

        return self.get_lowest_f_score_from_opened_list()

    def get_lowest_f_score_from_opened_list(self):

        self.opened_list = CasesList(sorted(self.opened_list, key=attrgetter('h')))
        # logger.info("Sorted opened_list %s" % self.opened_list)

        return self.opened_list[0]

    def compute_list_potential_next_case(self, current_case, target):

        list_potential_next_case = CasesList()
        for x in (1, 0, -1):  # try shuffling here in order to have a decision less geometrical
            for y in (1, 0, -1):
                next_case = PotentialAstarNextCase(self.conf, self.level, current_case.case_x + x,
                                                   current_case.case_y + y, None, None, None, current_case)
                if next_case.is_valid():
                    if fabs(x) == fabs(y): continue  # only vert / horiz movement

                    if next_case in self.closed_list:
                        continue
                    h = self.get_manhattan_distance_to_target(next_case, target)
                    g = next_case.parent_case.g + MOVEMENT_COST
                    f = h + g
                    next_case.h = h
                    next_case.g = g
                    next_case.f = f

                    if next_case not in self.opened_list:
                        self.opened_list.append(next_case)
                    else:

                        # we get the case in the opening list corresponding to the calculated case for f value comparison
                        for index, item in enumerate(self.opened_list):
                            if item.case_x == next_case.case_x and item.case_y == next_case.case_y:
                                corresponding_case_in_opened_list = item
                                index_of_corresponding_case_in_opened_list = index

                        if next_case.f < corresponding_case_in_opened_list.f:
                            corresponding_case_in_opened_list.f = next_case.f
                            corresponding_case_in_opened_list.parent = next_case.parent_case
                            self.opened_list[
                                index_of_corresponding_case_in_opened_list] = corresponding_case_in_opened_list

    def get_manhattan_distance_to_target(self, next_case_position, target):

        distance = fabs(target.case.case_x - next_case_position.case_x) + fabs(
            target.case.case_y - next_case_position.case_y)

        return distance

    def get_found_path(self, start, target):

        closed_list_copy = self.closed_list.copy()
        closed_list_copy.reverse()

        current_case = closed_list_copy.pop(0)
        found_path = CasesList()
        found_path.append(current_case)
        x = True
        while x:

            case = next((x for x in closed_list_copy if (current_case.parent_case is not None
                                                         and current_case.parent_case.case_x == x.case_x
                                                         and current_case.parent_case.case_y == x.case_y)), False)

            if case:
                # print("%s,%s a pour parent %s,%s" %(current_case.case_x, current_case.case_y, case.case_x, case.case_y))
                found_path.append(case)
                closed_list_copy.pop(0)
                current_case = case
                print("current case %s : start case %s" % (current_case, start.case))
                if current_case == start.case:
                    print("PATH CALCULATION FINISHED")
                    return found_path
                else:
                    print("PATH CALCULATION NOT FINISHED")
            else:
                print("no case left")
                return None
