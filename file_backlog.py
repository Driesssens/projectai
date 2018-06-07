import os


def name(file_name):
    return os.path.splitext(file_name)[0]


class FileBacklog:
    def __init__(self, output_folder, configuration):
        input_folder = "input/{}".format(configuration.input_set)
        output_files = set(map(name, os.listdir(output_folder)))
        input_files = set(map(name, os.listdir(input_folder)))
        self.backlog = list(input_files - output_files)
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index >= len(self.backlog):
            raise StopIteration
        else:
            self.index += 1
            return self.backlog[self.index - 1]
