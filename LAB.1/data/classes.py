import os


class Class:
    def __init__(self, path, name, line, body=None):
        self.path = os.path.normpath(path)
        self.name = name
        self.line = line
        self.body = body

        self.__subclasses = list()
        self.__methods = list()
