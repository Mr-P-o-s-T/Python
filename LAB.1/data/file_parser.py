from .classes import Class
import os


class FileParser:
    def __init__(self, snippet, path, class_name=None):
        self.stack = list()
        self.__methods = list()
        self.__comments = list()
        self.__subclasses = list()
        self.__includes = list()

        self.index = 0
        self.line = 1
        self.number = 0
        self.start_line = 0

        self.body = str()
        self.comment = str()

        self.snippet = snippet
        self.class_name = class_name

        self.is_clang_comment = False
        self.is_cpp_comment = False
        self.is_function = False

        self.path = os.path.normpath(path)

    def parse(self):
        pass

    def parse_multiline_comment(self):
        pass

    def parse_single_line_comment(self):
        pass

    def parse_macros(self):
        pass

    def parse_include(self):
        pass

    def parse_function(self):
        pass

    def parse_struct(self):
        pass

    def parse_class(self):
        pass

    def parse_template(self):
        pass
