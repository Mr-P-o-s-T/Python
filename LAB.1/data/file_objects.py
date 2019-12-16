from .parser_helper import Helper


class FileObject:
    _string_substitute = {
        '<': '&lt',
        '>': '&gt',
        'struct': 'Structure',
        'class': 'Class',
        'union': 'Union'
    }

    def _substitute(self, string: str):
        try:
            return self._string_substitute[string]
        except KeyError:
            return string

    def _subst_gt_ls_(self, strings: list):
        res = ''
        for i in range(len(strings)):
            if i > 0:
                res += ', '
            tmp = strings[i].split('<')
            tmp = self._substitute('<').join(tmp)
            tmp = tmp.split('>')
            res += self._substitute('>').join(tmp)
        return res

    def __init__(self, name: str, namespaces: str):
        self.name = name
        self.namespaces = self._subst_gt_ls_([namespaces])
        self._comments = []
        self.__default_comment = ''

    @property
    def def_comment(self):
        return self.__default_comment

    @def_comment.setter
    def def_comment(self, value: str):
        self.__default_comment = value

    @property
    def comment_list(self) -> str:
        if not self.has_comments():
            self.comment_list = [(Helper.multiline, self.__default_comment)]
        return '<br />'.join([x[1] for x in self._comments])

    @comment_list.setter
    def comment_list(self, comment_block: list):
        for comment in comment_block:
            if comment[0] == Helper.multiline:
                tmp = comment[1].split('\n')
                comment = (comment[0], '<br />'.join(tmp))
            self._comments.append(comment)

    @property
    def body(self):
        return self._body_get()

    def _body_get(self):
        pass

    @body.setter
    def body(self, value):
        self._body_set(value)

    def _body_set(self, value: str):
        pass

    def has_comments(self) -> bool:
        return len(self._comments) > 0

    def parse(self):
        pass

    def _preparation(self):
        pass

    @staticmethod
    def split_define(define: tuple) -> (str, str):
        tmp = define[1] + ' ' + define[2]
        tmp = tmp.split('\n', 1)
        if len(tmp) == 1:
            tmp.append('')
        return tuple(tmp)

    @staticmethod
    def generate_namespace(namespace: str):
        tmp = namespace.split('::')
        return '<span class="text-separator">::</span>'.join(tmp)

    def generate_index(self) -> list:
        res = list()
        res.append((self.namespaces, self.name))
        return res
