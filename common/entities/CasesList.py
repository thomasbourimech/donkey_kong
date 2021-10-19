class CasesList(list):

    def __str__(self):
        str_output = ""
        for case in self:
            str_output += case.__str__() + "\n"
        return "\n" + str_output[0:len(str_output)-1]

    def draw_list_case(self, window, color):

        for case in self:
            case.draw_case(window, color)