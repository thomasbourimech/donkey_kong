from common.Case import Case

class PotentialNextCase(Case):

    def __init__(self, conf, level, case_x, case_y, pathfinder):
        super().__init__(conf, level, case_x, case_y)
        self.conf = conf
        self.distance = None
        self.nb_visit = self.count_nb_of_visite_for_case(pathfinder.cases_visited)

    def count_nb_of_visite_for_case(self, pathfinder_cases_visited):

        count = 0
        for case in pathfinder_cases_visited:

            if case == self:
                count += 1

        return count

    def __str__(self):
        return super().__str__() + ", d=" + str(self.distance) + ", visited=" + str(self.nb_visit)