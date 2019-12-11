from .parser_helper import Helper
from . import FileObject

arrays_default_comment = "This is a '{}': array of '{}' type, with number of elements = {}{}but it has no " \
                         "additional commentaries yet"
variables_default_comment = "This is a '{}': {} of '{}' type{}but it has no additional commentaries yet"
variable_description = '<div class="h3 border-bottom">\n<span class="text-type">{}</span>\n' \
                       '<span><span class="text-namespaces">{}</span>{}{}</span></div>\n' \
                       '<div class="container text-comment">\n{}\n</div>'


class Variable(FileObject):
    def __init__(self, info: tuple, is_class_member: bool = False, namespaces: str = ''):
        super().__init__(info[3], namespaces)
        self.type = info[1]
        self.pointer = info[2]
        self.is_array = info[0] == Helper.array
        if info[4] == '':
            self.array_capacity = 'size of initializer'
        else:
            self.array_capacity = info[4]
        self.initializer = info[5]
        self.is_field = is_class_member

        if self.is_array:
            self.def_comment = arrays_default_comment.\
                format(self.name,
                       self.type + self.pointer,
                       self.array_capacity,
                       ('<br />initialized with: <pre>' + self.initializer + '</pre>', ', ')[self.initializer == ''])
        else:
            self.def_comment = variables_default_comment.\
                format(self.name,
                       ('value', 'pointer')[self.pointer != ''],
                       self.type,
                       ('<br />initialized with: <pre>' + self.initializer + '</pre>', ', ')[self.initializer == ''])

    def __str__(self):
        return variable_description.format(self.type + self.pointer, self.generate_namespace(self.namespaces),
                                           self.name, ('', '[' + self.array_capacity + ']')[self.is_array],
                                           self.comment_list)
