from .parser_helper import Helper
from . import *


class Namespace(Class):
    def __init__(self, info: tuple, namespaces_: str = '', default_comment: str = ''):
        super().__init__(info, namespaces_, default_comment)

        self.subnamespaces = dict()

    def parse(self):
        super().parse()

    def generate_classes(self, i: int = 0) -> (str, int):
        res, i = super().generate_classes(i)
        for x in self.subnamespaces:
            res += self.subnamespaces[x].generate_classes(i)[0]
        return res, i

    def generate_index(self) -> list:
        res = []
        for x in self.subnamespaces:
            res += self.subnamespaces[x].generate_index()
        for x in self.subclasses:
            res += self.subclasses[x].generate_index()
        for x in self.functions:
            res += self.functions[x].generate_index()
        for x in self.variables:
            res += self.variables[x].generate_index()
        return res

    @staticmethod
    def search_in_subbodies(area_, namespaces_: str):
        while namespaces_ != '':
            name, namespaces_ = Helper.slice_long_id(namespaces_)
            if name in area_.subclasses:
                area_ = area_.subclasses[name]
            else:
                area_ = area_.subnamespaces[name]
        return area_

    @staticmethod
    def process_namespace(class_, comments_block, x: tuple):
        tmp = Namespace(x, class_.namespaces + '::' + class_.name)
        class_.subnamespaces.update({x[1]: tmp})
        tmp.parse()

    @staticmethod
    def process_function(area_, comments_block, x: tuple, is_method: bool = False):
        name, namespaces_ = Helper.slice_long_id(x[2])
        area_ = area_.search_in_subbodies(area_, namespaces_)
        super().process_function(area_, comments_block, x, is_method)

    @staticmethod
    def process_template_function(area_, comments_block, x: tuple, is_method: bool = False):
        name, namespaces_ = Helper.slice_long_id(x[4])
        area_ = area_.search_in_subbodies(area_, namespaces_)
        super().process_template_function(area_, comments_block, x, is_method)

    @staticmethod
    def process_variable(class_, comments_block: list, x: tuple, is_field: bool = False):
        super().process_variable(class_, comments_block, x, is_field)

    def __str__(self):
        return ''
