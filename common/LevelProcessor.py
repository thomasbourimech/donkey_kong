class levelGrid:

    def __init__(self, path_to_level_file):

        self.path_to_level_file = path_to_level_file
        self.level = self.read_level_file(path_to_level_file)
        self.level_grid_width = self.read_level_width()
        self.level_grid_height = self.read_level_height()

    def __str__(self):

        return str(self.level)

    def read_level_file(self, path_to_level_file):

        with open(path_to_level_file, "r") as file:
            level = []
            for line in file:
                level_line = []
                for sprite in line:

                    if sprite != "\n":
                        level_line.append(sprite)

                level.append(level_line)

        return level

    def read_level_height(self):

        return len(self.level)

    def read_level_width(self):

        return len(self.level)






