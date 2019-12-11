import re


class Helper:
    access = 'access'
    oneline = 'oneline'
    multiline = 'multiline'
    function_decl = 'function decl'
    friend_function_decl = 'friend function decl'
    function_def = 'function'
    declaration = ' decl'
    array = 'array'
    arrays = 'arrays'
    variable = 'variable'
    variables = 'variables'
    class_def = 'class'
    class_decl = 'class decl'
    friend_class_decl = 'friend class decl'
    struct_def = 'struct'
    struct_decl = 'struct decl'
    union_def = 'union'
    union_decl = 'union decl'
    using = 'using'
    namespace = 'namespace'
    inline_namespace = 'inline namespace'
    template = 'template'
    file = 'file'
    define = 'define'
    include = 'include'

    __space_tab = r"[\t ]"
    __name_sep = r"::"
    __id = r"[a-zA-z_]\w*"
    __long_id = r"[a-zA-z_](?:\w|{}|<[^<>]+>)*".format(__name_sep)
    __type_id = r"(?:(?:const|volatile|mutable|register|static|extern){}+)?(?:(?:unsigned|signed|long|short){}+)*{}". \
        format(__space_tab, __space_tab, __long_id)

    __name_sep_pattern = re.compile(__name_sep)

    __one_line_comment = r"{}*//{}*(.*)\s".format(__space_tab, __space_tab)
    __multiline_comment = r"{}*/\*\s*([\s\S]*?)\s*\*/\s".format(__space_tab)
    __one_line_comment_pattern = re.compile(__one_line_comment)
    __multiline_comment_pattern = re.compile(__multiline_comment)

    __body = "{}"
    __template_args = "<>"
    __function_params = "()"

    __patterns = dict()

    __args_list = r"\s*,\s*"
    __pointer = r"([*&]+)?"
    __args_list_patterns = re.compile(__args_list)

    __array_header = r"{}*({}){}(.+?)\s*=\s*$".format(__space_tab, __type_id, __pointer + r"{}+".format(__space_tab))
    __function_header = r"{}*(?:inline\s+)?((?:{})\s*(?:[*&]+)?)\s+({}|operator.{})\s*\(([^()]*?)\)\s*$".\
        format(__space_tab, __type_id, __long_id, '{1,2}')
    __namespace_header = r"{}*((?:inline\s)?namespace)\s+({})\s*$".format(__space_tab, __long_id)
    __class_header = r"{}*(class|struct|union)\s+({})\s*$".format(__space_tab, __long_id)
    __class_array_ending_1 = r"^\s*(.+\s*=\s*)$"
    __class_array_ending_2 = r"^\s*(.*)\s*;"
    __template = r"{}*(template)\s+<([\s\S]*)>\s*$".format(__space_tab)
    __array_header_pattern = re.compile(__array_header)
    __function_header_pattern = re.compile(__function_header)
    __namespace_header_pattern = re.compile(__namespace_header)
    __class_header_pattern = re.compile(__class_header)
    __class_array_ending_1_pattern = re.compile(__class_array_ending_1)
    __class_array_ending_2_pattern = re.compile(__class_array_ending_2)
    __template_pattern = re.compile(__template)

    __include = r"{}*#(include)\s+([<\"].*?[\">])".format(__space_tab)
    __define = r"{}*#(define){}+({}(?:\(.+\))?){}*((?:\\\n|[^\\\n])*)".format(__space_tab, __space_tab, __id,
                                                                              __space_tab)
    __include_pattern = re.compile(__include)
    __define_pattern = re.compile(__define)

    __variable_decl = r"{}*({}){}([\s\S]+?);".format(__space_tab, __type_id, __pointer + r"\s+")
    __function_declaration = r"{}*(?:(friend\s)\s*)?((?:{})\s*(?:[*&]+)?)\s+({}|operator.{})\s*\(([^()]*?)\)\s*;".\
        format(__space_tab, __type_id, __long_id, '{1,2}')
    __class_declaration = r"{}*(?:(friend\s)\s*)?(class|structure|union)\s+({})\s*;".format(__space_tab, __long_id)
    __variable_init = r"^{}({})(?:(\[.*\]))?(?:\s*=\s*([\s\S]+)?)?$".format(__pointer + r"\s*", __long_id)
    __variable_decl_pattern = re.compile(__variable_decl)
    __function_decl_pattern = re.compile(__function_declaration)
    __class_decl_pattern = re.compile(__class_declaration)
    __variable_init_pattern = re.compile(__variable_init)

    __access_modifier = r"{}*(private|protected|public):".format(__space_tab)
    __access_modifier_pattern = re.compile(__access_modifier)

    __using = r"{}*(using)\s+(.+)\s*;".format(__space_tab, __id)
    __using_pattern = re.compile(__using)

    @staticmethod
    def __is_tuple(x):
        return type(x) == tuple

    @staticmethod
    def __is_non_empty_str(x):
        return x != ''

    @staticmethod
    def __get_pattern(bracks: str):
        try:
            return Helper.__patterns[bracks]
        except KeyError:
            Helper.__patterns.update({bracks: re.compile(r"[{}]".format(bracks))})

        return Helper.__patterns[bracks]

    @staticmethod
    def __insert_splitter_content(content_list: list, splitter_content: list, res: list, res_def_name: str = ''):
        for i in range(len(content_list) - 1, -1, -1):
            if Helper.__is_tuple(content_list[i]):
                continue
            content_list[i] = splitter_content[-1][-1]
            for j in range(len(res[-1]) - 1, -1, -1):
                content_list.insert(i, ((res_def_name,) + res[-1][j], res[-1][j])[res_def_name == ''])
                content_list.insert(i, splitter_content[-1][j])
            del splitter_content[-1]
            del res[-1]

        tmp = list(filter(Helper.__is_non_empty_str, content_list))
        content_list.clear()
        content_list += tmp
        # Helper.__separate_tuples_(content_list)

    @staticmethod
    def __extract_comments(content_list: list):
        comment_groups = list()
        res_content_list = list()
        for x in content_list:
            if Helper.__is_tuple(x):
                continue
            comments = list()
            res_content_list.append([])
            i = int()
            multiline_comments = Helper.__multiline_comment_pattern.findall(x)
            splitter_content = Helper.__multiline_comment_pattern.split(x)
            splitter_content = [splitter_content[i] for i in range(len(splitter_content)) if i % 2 == 0]
            for j in range(len(splitter_content)):
                if j > 0:
                    comments.append((Helper.multiline, multiline_comments[i]))
                    i += 1
                one_line_comments = Helper.__one_line_comment_pattern.findall(splitter_content[j])
                tmp = Helper.__one_line_comment_pattern.split(splitter_content[j])
                tmp = [tmp[i] for i in range(len(tmp)) if i % 2 == 0]
                res_content_list[-1] += tmp
                for y in one_line_comments:
                    comments.append((Helper.oneline, y))
            comment_groups.append(comments)

        Helper.__insert_splitter_content(content_list, res_content_list, comment_groups)

    @staticmethod
    def __extract_bodies(content_list: list):
        Helper.__extract_closed_brackets(content_list, Helper.__body)
        Helper.__determine_bodies(content_list)

    @staticmethod
    def __extract_list_with_brackets(content_list: list, bracks: str):
        content_list[0] = Helper.__extract_args_list(content_list[0])
        for i in range(1, len(content_list), 2):
            content_list[i + 1] = Helper.__extract_args_list(content_list[i + 1])
            content_list[i - 1][-1] += bracks[0] + content_list[i] + bracks[-1] + content_list[i + 1][0]
            content_list[i] = ''
            del content_list[i + 1][0]
        tmp = [x for i in range(0, len(content_list), 2) for x in content_list[i]]

        content_list.clear()
        content_list += tmp

    @staticmethod
    def __extract_template_args(template_list: list):
        Helper.__extract_closed_brackets(template_list, Helper.__template_args)
        Helper.__extract_list_with_brackets(template_list, Helper.__template_args)

    @staticmethod
    def __extract_round_brackets(content: list):
        Helper.__extract_closed_brackets(content, Helper.__function_params)
        Helper.__extract_list_with_brackets(content, Helper.__function_params)

    @staticmethod
    def __extract_function_args(args: str) -> list:
        args = [args]
        Helper.__extract_template_args(args)
        return args

    @staticmethod
    def __extract_args_list(args_list: str) -> list:
        return Helper.__args_list_patterns.split(args_list)

    @staticmethod
    def __extract_closed_brackets(content_list: list, bracks: str):
        pattern = Helper.__get_pattern(bracks)

        balance = int()
        bodies_list = list()
        splitter_content = list()

        for i in range(len(content_list)):
            brackets = pattern.findall(content_list[i])
            splitter_content += pattern.split(content_list[i])

            if len(brackets):
                for j in range(len(brackets)):
                    if balance > 0:
                        bodies_list[-1] += splitter_content[j] + brackets[j]
                        splitter_content[j] = ''
                    elif balance == 0:
                        if j > 0:
                            bodies_list[-1] = bodies_list[-1][:-1]
                        bodies_list.append('')

                    balance += (-1, 1)[brackets[j] == bracks[0]]

                if bodies_list[-1][-1] == bracks[1]:
                    bodies_list[-1] = bodies_list[-1][:-1]

        splitter_content = [splitter_content[i] for i in range(len(splitter_content)) if
                            splitter_content[i] != '' or i == (
                                    len(splitter_content) - 1)]
        content_list.clear()
        for i in range(len(bodies_list)):
            content_list.append(splitter_content[i])
            content_list.append(bodies_list[i])
        content_list.append(splitter_content[len(bodies_list)])

    @staticmethod
    def __extract_templates_declaration(content_list: list, i: int):
        if not Helper.__is_tuple(content_list[i - 1]):
            header = Helper.__template_pattern.findall(content_list[i - 1])
            if len(header) != 0:
                content_list[i - 1] = Helper.__template_pattern.split(content_list[i - 1])[0]
                args = [header[0][1]]
                Helper.__extract_template_args(args)
                content_list[i] = (header[0][0], args) + content_list[i]

    @staticmethod
    def __determine_bodies(content_list: list):
        for i in range(1, len(content_list), 2):
            header = Helper.__namespace_header_pattern.findall(content_list[i - 1])
            if len(header):
                content_list[i - 1] = Helper.__namespace_header_pattern.split(content_list[i - 1])[0]
                content_list[i] = header[0] + (content_list[i],)
            else:
                header = Helper.__function_header_pattern.findall(content_list[i - 1])
                if len(header) != 0:
                    content_list[i - 1] = Helper.__function_header_pattern.split(content_list[i - 1])[0]
                    content_list[i] = (Helper.function_def, header[0][0], header[0][1]) + \
                                      (Helper.__extract_function_args(header[0][2]),) + (content_list[i],)
                else:
                    header = Helper.__class_header_pattern.findall(content_list[i - 1])
                    if len(header) != 0:
                        content_list[i - 1] = Helper.__class_header_pattern.split(content_list[i - 1])[0]
                        content_list[i] = header[0] + (content_list[i],)
                        tmp = list()
                        Helper.__extract_variables_list_with_initializations(content_list, i, tmp)
                    else:
                        header = Helper.__array_header_pattern.findall(content_list[i - 1])
                        if len(header) != 0:
                            content_list[i - 1] = Helper.__array_header_pattern.split(content_list[i - 1])[0]
                            tmp = list()
                            content = [header[0][2]]
                            Helper.__extract_round_brackets(content)
                            content[-1] += ' = {' + content_list[i] + '}'
                            tmp += content
                            content_list[i] = (Helper.arrays, header[0][0], header[0][1])
                            Helper.__extract_variables_list_with_initializations(content_list, i, tmp)
                Helper.__extract_templates_declaration(content_list, i)

        tmp = list(filter(Helper.__is_non_empty_str, content_list))
        content_list.clear()
        content_list += tmp
        # Helper.__separate_tuples_(content_list)

    @staticmethod
    def __extract_variables_list_with_initializations(content_list, i, tmp):
        shift = 1
        tail = Helper.__class_array_ending_1_pattern.findall(content_list[i + 2 * shift - 1])
        while len(tail) != 0:
            content_list[i + 2 * shift - 1] = ''
            content = [tail[0]]
            Helper.__extract_round_brackets(content)
            content[-1] += '{' + content_list[i + 2 * shift] + '}'
            tmp += content
            content_list[i + 2 * shift] = ''
            shift += 1
            tail = Helper.__class_array_ending_1_pattern.findall(content_list[i + 2 * shift - 1])
        tail = Helper.__class_array_ending_2_pattern.findall(content_list[i + 2 * shift - 1])
        content_list[i + 2 * shift - 1] = Helper.__class_array_ending_2_pattern.split(
            content_list[i + 2 * shift - 1])[-1]
        content = [tail[0]]
        Helper.__extract_round_brackets(content)
        tmp += content
        content_list[i] += (list(filter(Helper.__is_non_empty_str, tmp)),)

    @staticmethod
    def __extract_macros(content_list: list) -> list:
        res = Helper.__extract_macro(content_list, Helper.__define_pattern)
        res += Helper.__extract_macro(content_list, Helper.__include_pattern)
        return res

    @staticmethod
    def __extract_macro(content_list: list, pattern) -> list:
        res = list()
        splitter_content = list()
        length = int(1)
        for i in range(len(content_list)):
            res += pattern.findall(content_list[i])
            tmp = pattern.split(content_list[i])
            if len(res) != 0:
                length = len(res[0]) + 1
            splitter_content += [tmp[length * i] for i in range(len(tmp) // length + (1, 0)[len(tmp) % length == 0])
                                 if tmp[length * i] != '']
        content_list.clear()
        content_list.append('')
        for x in splitter_content:
            content_list[0] += x
        return res

    @staticmethod
    def __extract_declarations(content_list: list, decl_pattern, res_def_name: str = ''):
        res = list()
        splitter_content = list()
        length = int(1)
        for x in content_list:
            if Helper.__is_tuple(x):
                continue
            res.append(decl_pattern.findall(x))
            tmp = decl_pattern.split(x)
            if len(res[-1]) != 0:
                length = len(res[-1][0]) + 1
            splitter_content.append(
                [tmp[length * i] for i in range(len(tmp) // length + (1, 0)[len(tmp) % length == 0])])

        Helper.__insert_splitter_content(content_list, splitter_content, res, res_def_name)

    @staticmethod
    def __process_variables(content_list: list):
        for i in range(len(content_list) - 1, -1, -1):
            if content_list[i][0] == Helper.class_def or content_list[i][0] == Helper.struct_def or \
                    content_list[i][0] == Helper.union_def:
                variables = content_list[i][3]
            elif content_list[i][0] == Helper.function_decl or content_list[i][0] == Helper.function_def or \
                    content_list[i][0] == Helper.friend_function_decl:
                variables = content_list[i][3]
                variables = [x + ';' for x in variables if Helper.__is_non_empty_str(x)]
                Helper.__extract_variables_decl(variables)
                content_list[i] = content_list[i][0:3] + (variables,) + content_list[i][4:]
                continue
            elif content_list[i][0] == Helper.template:
                if content_list[i][2] == Helper.class_def or content_list[i][2] == Helper.struct_def or \
                        content_list[i][2] == Helper.union_def:
                    variables = content_list[i][5]
                elif content_list[i][2] == Helper.function_decl or content_list[i][2] == Helper.function_def or \
                        content_list[i][2] == Helper.friend_function_decl:
                    variables = content_list[i][5]
                    variables = [x + ';' for x in variables if Helper.__is_non_empty_str(x)]
                    Helper.__extract_variables_decl(variables)
                    content_list[i] = content_list[i][0:5] + (variables,) + content_list[i][6:]
                    continue
            else:
                if content_list[i][0] != Helper.variables and content_list[i][0] != Helper.arrays:
                    continue
                if content_list[i][0] == Helper.arrays:
                    variables = content_list[i][3]
                else:
                    variables = [content_list[i][3]]
                    Helper.__extract_round_brackets(variables)
                variables[0] = content_list[i][2] + variables[0]

            for variable in variables:
                tmp_i = Helper.__variable_init_pattern.findall(variable)[0]
                if tmp_i[2] == '':
                    content_list.insert(i + 1, (Helper.variable, content_list[i][1]) + tmp_i)
                else:
                    content_list.insert(i + 1, (Helper.array, content_list[i][1]) + tmp_i[0:2] + (tmp_i[2][1:-1],) +
                                        tmp_i[3:])

            if content_list[i][0] == Helper.class_def or content_list[i][0] == Helper.struct_def or \
                    content_list[i][0] == Helper.union_def or content_list[i][0] == Helper.template:
                content_list[i] = content_list[i][:-1]
            else:
                del content_list[i]

    @staticmethod
    def __extract_classes_decl(content_list: list):
        Helper.__extract_declarations(content_list, Helper.__class_decl_pattern, Helper.declaration)
        for i in range(len(content_list)):
            if content_list[i][0] == Helper.declaration:
                content_list[i] = (content_list[i][1] + content_list[i][2] + content_list[i][0],) + content_list[i][3:]
                Helper.__extract_templates_declaration(content_list, i)

    @staticmethod
    def __extract_functions_decl(content_list: list):
        Helper.__extract_declarations(content_list, Helper.__function_decl_pattern, Helper.function_decl)
        for i in range(len(content_list)):
            if content_list[i][0] == Helper.function_decl:
                if content_list[i][1] == 'friend ':
                    content_list[i] = (Helper.friend_function_decl,) + content_list[i][2:4] + \
                                      (Helper.__extract_function_args(content_list[i][4]),) + content_list[i][5:]
                else:
                    content_list[i] = (Helper.function_decl,) + content_list[i][2:4] + \
                                      (Helper.__extract_function_args(content_list[i][4]),) + content_list[i][5:]
                Helper.__extract_templates_declaration(content_list, i)

    @staticmethod
    def __extract_variables_decl(content_list: list):
        Helper.__extract_declarations(content_list, Helper.__variable_decl_pattern, Helper.variables)
        Helper.__process_variables(content_list)

    @staticmethod
    def __extract_usages(content_list: list):
        Helper.__extract_declarations(content_list, Helper.__using_pattern, '')

    @staticmethod
    def __extract_access_modifiers(content_list: list):
        modifiers = list()
        splitter_content = list()
        for j in range(len(content_list)):
            if Helper.__is_tuple(content_list[j]):
                continue
            modifiers += Helper.__access_modifier_pattern.findall(content_list[j])
            tmp = Helper.__access_modifier_pattern.split(content_list[j])
            splitter_content.append([tmp[2 * i] for i in range(len(tmp) // 2 + (1, 0)[len(tmp) % 2 == 0])])

        bodies_list = [content_list[i] for i in range(1, len(content_list), 2)]
        content_list.clear()
        for i in range(len(bodies_list)):
            if splitter_content[i][0] != '':
                content_list.append(splitter_content[i][0])
            for j in range(1, len(splitter_content[i])):
                content_list.append((Helper.access, modifiers[0]))
                del modifiers[0]
                if splitter_content[i][j] != '':
                    content_list.append(splitter_content[i][j])
            content_list.append(bodies_list[i])
        if splitter_content[-1][0] != '':
            content_list.append(splitter_content[-1][0])
        for j in range(1, len(splitter_content[-1])):
            content_list.append((Helper.access, modifiers[0]))
            del modifiers[0]
            if splitter_content[-1][j] != '':
                content_list.append(splitter_content[-1][j])

    @staticmethod
    def slice_long_id(long_id: str) -> (str, str):
        tmp = Helper.__name_sep_pattern.split(long_id)
        return tmp[-1], '::'.join(tmp[:-1])

    @staticmethod
    def slice_content(content: str):
        if content is not None:
            content = [content]
            macros = Helper.__extract_macros(content)

            Helper.__extract_bodies(content)
            Helper.__extract_usages(content)
            Helper.__extract_access_modifiers(content)

            Helper.__extract_comments(content)
            Helper.__extract_functions_decl(content)
            Helper.__extract_classes_decl(content)
            Helper.__extract_variables_decl(content)

            return content, macros
        return [], []
