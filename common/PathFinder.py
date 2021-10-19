from common.entities.PotentialNextCase import PotentialNextCase
from common.entities.CasesList import CasesList
from math import sqrt, fabs
import logging
from operator import attrgetter

logger = logging.getLogger("DonkeyKong")


class PathFinder:

    def __init__(self, conf, level, orig):

        self.conf = conf
        self.level = level
        self.orig = orig
        self.current_case = self.orig.case
        self.cases_visited = []
        self.cases_to_visit = []
        self.previous_target_case = None
        self.append_case_to_visited_list(self.current_case)


    def compute_full_path(self, target):

        #We reset the list of case visited in case of target changing position (killa feature)
        if self.previous_target_case is not None:
            if self.previous_target_case != target.case:
                logger.info("Target has changed his position...Resetting pathfinder.cases_visited to []")
                self.cases_visited = []


        if (self.orig.is_same_position(target)):
            logger.info("target: %s : " %target)
            logger.info("orig: %s : " % self.orig)


        else:
            logger.info("target: %s : " % target)
            logger.info("orig: %s : " % self.orig)
            logger.info("continuing")
            next_case = self.compute_next_case(target)
            logger.info(self.cases_visited)
            self.append_case_to_visited_list(next_case)
            self.current_case = next_case
            self.orig.case = next_case
            self.previous_target_case = target.case
        return (self.cases_visited, self.cases_to_visit)


    def append_case_to_visited_list(self, case):

        if case not in self.cases_visited:
            self.cases_visited.append(case)

    def compute_next_case(self, target):

        logger.info("============New next positions sets computation initiated=============")
        logger.info("Moves originate from %s", self.current_case)
        logger.info("list of points and their distance to target %s" % target)
        list_potential_next_case = CasesList()
        for x in (1, 0, -1): #try shuffling here in order to have a decision less geometrical
            for y in (1, 0, -1):
                next_case = PotentialNextCase(self.conf, self.level, self.current_case.case_x + x, self.current_case.case_y + y,
                                              self)
                #if next_case.is_in_boundaries and next_case.case_type != "1":
                if next_case.is_valid():
                    if not (fabs(x) == fabs(y)): #only vert / horiz movement
                        #logger.info("---------------")
                        #logger.info("x:%s", x)
                        #logger.info("y:%s", y)
                        next_case.distance = self.get_distance_to_target(next_case, target)
                        list_potential_next_case.append(next_case)
                        self.cases_to_visit.append(next_case)



        most_suitable_case = self.select_most_suitable_next_position(list_potential_next_case)

        return most_suitable_case

    def sort_list_potential_next_case(self, list_potential_next_case):

        list_potential_next_case = CasesList(sorted(list_potential_next_case, key=attrgetter('nb_visit','distance')))

        logger.info("Sorted list : %s " % list_potential_next_case)

        return list_potential_next_case

    def select_most_suitable_next_position(self, list_potential_next_case):

        list_potential_next_case = self.sort_list_potential_next_case(list_potential_next_case)

        case_selected = list_potential_next_case[0]
        self.cases_visited.append(case_selected)
        logger.info("Most suitable case: %s" % case_selected)
        case_selected.nb_visit += 1

        return case_selected

    def get_distance_to_target(self, next_case_position, target):

        distance = fabs(sqrt(((target.case.case_x - next_case_position.case_x)**2
                              + (target.case.case_y - next_case_position.case_y)**2)))

        return distance

