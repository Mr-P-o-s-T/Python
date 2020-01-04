from .parser_helper import Helper
import data.file_objects as def_comments
from . import *

class_default_comment = "This is a '{}': {}{}, but it has no additional commentaries yet"
template_class_default_comment = "This is a '{}': template of {}{}, with <br />{} parameters, but it has no " \
                                 "additional commentaries yet "
class_description = ('<div class="container">\n'
                     '<div class="h3 border-bottom">\n'
                     '<span class="text-type">{}</span>\n'
                     '<span><span class="text-namespaces">{}</span>{}</span>\n'
                     '</div>\n'
                     '<div class="container text-comment">\n'
                     '{}\n'
                     '</div>\n'
                     '{}'
                     '</div>')
template_class_description = ('<div class="container">\n'
                              '<div class="h3 border-bottom">\n'
                              '<span class="text-type">template &lt{}&gt</span><br />\n'
                              '<span class="text-type">{}</span>\n'
                              '<span><span class="text-namespaces">{}</span>{}</span>\n'
                              '</div>\n'
                              '<div class="container text-comment">\n'
                              '{}\n'
                              '</div>\n'
                              '{}'
                              '</div>')
class_members_description = ('<h3 class="border-bottom">Subclasses:</h3>\n'
                             '<div class="p-3 container bg-white">\n'
                             '{}\n'
                             '</div>\n'
                             '<h3 class="border-bottom">Methods:</h3>\n'
                             '<div class="p-3 container bg-white">\n'
                             '{}\n'
                             '</div>\n'
                             '<h3 class="border-bottom">Variables:</h3>\n'
                             '<div class="p-3 container bg-white">\n'
                             '{}\n'
                             '</div>\n')


class Class(FileObject):
    def __init__(self, info: tuple, namespaces_: str = '', default_comment: str = class_default_comment):
        self.type = info[0].split()[0]
        name, namespace = Helper.slice_long_id(info[1])
        super().__init__(name, namespaces_ + namespace)
        if len(info) == 2:
            self.body_ = None
        else:
            self.body_ = info[2]

        self.subclasses = dict()
        self.functions = dict()
        self.variables = dict()

        self.def_comment = default_comment.format(self.name, self.type, ('', ' declaration')[len(info) == 2])

    def parse(self):
        comments_block = list()
        content = self._preparation()

        for x in content:
            if type(x) != tuple:
                comments_block.clear()
                continue
            type_ = x[0]
            if type_ == Helper.oneline:
                comments_block.append(x)
            elif type_ == Helper.multiline:
                comments_block.clear()
                comments_block.append(x)
            elif type_ == Helper.class_def or type_ == Helper.struct_def or type_ == Helper.union_def or \
                    type_ == Helper.class_decl or type_ == Helper.struct_decl or type_ == Helper.union_decl:
                self.process_class(self, comments_block, x)
            elif type_ == Helper.function_def or type_ == Helper.function_decl:
                self.process_function(self, comments_block, x)
            elif type_ == Helper.variable or type_ == Helper.array:
                self.process_variable(self, comments_block, x)
            elif type_ == Helper.namespace or type_ == Helper.inline_namespace:
                self.process_namespace(self, comments_block, x)
            elif type_ == Helper.template:
                type_ = x[2]
                if type_ == Helper.class_def or type_ == Helper.struct_def or type_ == Helper.union_def or \
                        type_ == Helper.class_decl or type_ == Helper.struct_decl or type_ == Helper.union_decl:
                    self.process_template_class(self, comments_block, x)
                elif type_ == Helper.function_def or type_ == Helper.function_decl:
                    self.process_template_function(self, comments_block, x)
            if type_ != Helper.oneline and type_ != Helper.multiline:
                comments_block.clear()
        super().parse()

    def generate_classes(self, i: int = 0) -> (str, int):
        res = ''
        for x in self.subclasses:
            if i > 0:
                res += '<br />'
            res += str(self.subclasses[x])
            i += 1
        return res, i

    def generate_functions(self) -> str:
        res = ''
        i = 0
        for x in self.functions:
            if i > 0:
                res += '<br />'
            res += str(self.functions[x])
            i += 1
        return res

    def generate_variables(self) -> str:
        res = ''
        i = 0
        for x in self.variables:
            if i > 0:
                res += '<br />'
            res += str(self.variables[x])
            i += 1
        return res

    def generate_index(self) -> list:
        res = super().generate_index()
        for x in self.subclasses:
            res += self.subclasses[x].generate_index()
        for x in self.functions:
            res += self.functions[x].generate_index()
        for x in self.variables:
            res += self.variables[x].generate_index()
        return res

    def _body_get(self):
        return self.body_

    def _body_set(self, value: str):
        self.body_ = value
        self.def_comment = class_default_comment. \
            format(self.name, self.type, ('', ' declaration')[value is None])

    def _preparation(self):
        return Helper.slice_content(self.body)[0]

    @staticmethod
    def search_in_subbodies(class_, namespaces_: str):
        while namespaces_ != '':
            name, namespaces_ = Helper.slice_long_id(namespaces_)
            if name in class_.subclasses:
                class_ = class_.subclasses[name]
        return class_

    @staticmethod
    def process_class(class_, comments_block: list, x: tuple):
        name, namespaces_ = Helper.slice_long_id(x[1])
        class_ = class_.search_in_subbodies(class_, namespaces_)
        if name in class_.subclasses:
            tmp = class_.subclasses[name]
            if len(x) == 2:
                tmp.body = None
            else:
                tmp.body = x[2]
        else:
            tmp = Class(x, class_.namespaces + class_.name + '::')
            class_.subclasses.update({name: tmp})
            tmp.comment_list = comments_block
        tmp.parse()

    @staticmethod
    def process_template_class(class_, comments_block: list, x: tuple):
        name, namespaces_ = Helper.slice_long_id(x[3])
        class_ = class_.search_in_subbodies(class_, namespaces_)
        if name in class_.subclasses:
            tmp = class_.subclasses[name]
            if len(x) == 4:
                tmp.body = None
            else:
                tmp.body = x[4]
        else:
            tmp = TemplateClass(x, class_.namespaces + class_.name + '::')
            class_.subclasses.update({name: tmp})
            tmp.comment_list = comments_block
        tmp.parse()

    @staticmethod
    def process_namespace(class_, comments_block, x: tuple):
        pass

    @staticmethod
    def process_function(class_, comments_block, x: tuple, is_method: bool = True):
        tmp = Function(x, is_method, class_.namespaces + class_.name + '::')
        name = tmp.generate_name()
        if name in class_.functions:
            tmp = class_.functions[name]
            if len(x) == 4:
                tmp.body = None
            else:
                tmp.body = x[4]
        else:
            class_.functions.update({name: tmp})
            tmp.comment_list = comments_block
            tmp.parse()

    @staticmethod
    def process_template_function(class_, comments_block, x: tuple, is_method: bool = True):
        tmp = TemplateFunction(x, is_method, class_.namespaces + class_.name + '::')
        name = tmp.generate_name()
        if name in class_.functions:
            tmp = class_.functions[name]
            if len(x) == 6:
                tmp.body = None
            else:
                tmp.body = x[6]
        else:
            class_.functions.update({name: tmp})
            tmp.comment_list = comments_block
            tmp.parse()

    @staticmethod
    def process_variable(class_, comments_block: list, x: tuple, is_field: bool = True):
        tmp = Variable(x, is_field, class_.namespaces + class_.name + '::')
        class_.variables.update({x[3]: tmp})
        tmp.comment_list = comments_block
        tmp.parse()

    def __str__(self):
        res = class_description.format(self._substitute(self.type), self.generate_namespace(self.namespaces), self.name,
                                       self.comment_list, (class_members_description, '')[self.body_ is None])
        res = res.format('{}', self.generate_functions(), self.generate_variables())

        j = 0
        for x in self.subclasses:
            if j > 0:
                res += '<br />'
            res = res.format(str(self.subclasses[x]) + '{}')
            j += 1

        return res.format('')


class TemplateClass(Class):
    def __init__(self, info: tuple, namespaces_: str = ''):
        self.template_args = self._subst_gt_ls_(info[1])
        super().__init__(info[2:], namespaces_, template_class_default_comment
                         .format('{}', '{}', ('', ' declaration')[len(info) == 4],
                                 self._subst_gt_ls_(self.template_args)))

    def _body_set(self, value: str):
        self.def_comment = template_class_default_comment. \
            format('{}', '{}', ('', ' declaration')[value is None], self._subst_gt_ls_(self.template_args))

    def __str__(self):
        res = template_class_description.format(self.template_args,
                                                self._substitute(self.type), self.generate_namespace(self.namespaces),
                                                self.name, self.comment_list,
                                                (class_members_description, '')[self.body_ is None])
        res = res.format('{}', self.generate_functions(), self.generate_variables())

        j = 0
        for x in self.subclasses:
            if j > 0:
                res += '<br />'
            res = res.format(str(self.subclasses[x]) + '{}')
            j += 1

        return res.format('')
