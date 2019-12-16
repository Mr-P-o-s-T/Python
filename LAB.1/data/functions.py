from .parser_helper import Helper
from . import FileObject

function_default_comment = "This is a '{}': function{}, that accepts <br />{} arguments, and returns '{}' type " \
                           "values, but it has no additional commentaries yet"
template_function_default_comment = "This is a '{}': template of function{}, with <br />'{}' parameters, " \
                                    "that accepts <br />{} arguments, and returns '{}' type values, but it has no " \
                                    "additional commentaries yet "
function_description = ('<div class="h3 border-bottom">\n'
                        '<span class="text-type">{}</span>\n'
                        '<span><span class="text-namespaces">{}</span>{}</span><span>({})</span></div>\n'
                        '<div class="container text-comment">\n{}\n</div>')
template_function_description = ('<div class="h3 border-bottom">\n'
                                 '<span class="text-type">template &lt{}&gt</span><br />\n'
                                 '<span class="text-type">{}</span>\n'
                                 '<span><span class="text-namespaces">{}</span>{}</span><span>({})</span></div>\n'
                                 '<div class="container text-comment">\n{}\n</div>')
comment_argument = '{} {}{}{}'
argument = '<span class="text-type">{} </span>{}{}{}'


class Function(FileObject):
    def __init__(self, info: tuple, is_class_member: bool = False, namespaces: str = '',
                 default_comment: str = function_default_comment):
        name, namespace = Helper.slice_long_id(info[2])
        super().__init__(name, namespaces + namespace)

        self.args = info[3]
        self.ret_type = self._subst_gt_ls_([info[1]])
        self.is_method = is_class_member

        self.def_comment = default_comment. \
            format(self.name, ('', ' declaration')[len(info) == 4], self._generate_arguments(comment_argument),
                   self.ret_type)

    def _body_get(self):
        return None

    def _body_set(self, value: str):
        self.def_comment = function_default_comment. \
            format(self.name, ('', ' declaration')[value is None], self._generate_arguments(comment_argument),
                   self._subst_gt_ls_([self.ret_type]))

    def _generate_arguments(self, args_format: str):
        if len(self.args) == 0:
            return ('', ' no')[args_format == comment_argument]

        res = '{}'
        j = 0
        for x in self.args:
            if j > 0:
                res = res.format(', {}')
            res = res.format(args_format.format(self._subst_gt_ls_([x[1]]) + x[2],
                                                x[3] + ('', '[' + x[4] + ']')[x[0] == Helper.array],
                                                (' = ', '')[x[5] == ''] + x[5], '{}'))
            j += 1
        return res.format('')

    def generate_name(self) -> str:
        func_name = self.name
        for x in self.args:
            func_name += '_' + x[1] + '_' + x[2]
        return func_name

    def __str__(self):
        res = function_description.format(self.ret_type, self.generate_namespace(self.namespaces), self.name, '{}',
                                          self.comment_list)
        res = res.format(self._generate_arguments(argument))

        return res


class TemplateFunction(Function):
    def __init__(self, info: tuple, is_class_member: bool = False, namespaces: str = ''):
        self.template_args = self._subst_gt_ls_(info[1])
        super().__init__(info[2:], is_class_member, namespaces, template_function_default_comment
                         .format('{}', '{}', self.template_args, '{}', '{}'))

    def _body_set(self, value: str):
        self.def_comment = template_function_default_comment. \
            format(self.name, ('', ' declaration')[value is None], self.template_args,
                   self._generate_arguments(comment_argument), self.ret_type)

    def __str__(self):
        res = template_function_description.format(self.template_args,
                                                   self.ret_type,
                                                   self.generate_namespace(self.namespaces), self.name, '{}',
                                                   self.comment_list)
        res = res.format(self._generate_arguments(argument))

        return res
