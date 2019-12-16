from .parser_helper import Helper
from . import *

import os

file_default_comment = "This is a '{}': {} file, but it has no file commentaries yet"
define = ('<pre class="p-3  font-weight-bold"><span class="d-flex">'
          '<span class="text-danger">#define </span><span>{}</span></span><span>{}</span></pre>')
include = ('<pre class="p-3 font-weight-bold"><span class="d-flex">'
           '<span class="text-warning">#include </span><span class="text-include">{}</span></span></pre>')


class FileParser(Namespace):
    def __init__(self, path):
        name = os.path.basename(path)
        input_file = open(path, 'r')
        body = input_file.read()
        input_file.close()

        super().__init__((Helper.file, '', body), default_comment=file_default_comment.
                         format(name, ("source", "header")[name.split('.')[-1] == 'h']))
        self.preprocessors = list()

    def parse(self):
        super().parse()

    def generate_defines(self) -> (str, int):
        res = ''
        i = 0
        for i in range(0, len(self.preprocessors)):
            if self.preprocessors[i][0] != Helper.define:
                break
            if i > 0:
                res += '<br />'
            tmp = self.split_define(self.preprocessors[i])
            res += define.format(tmp[0], tmp[1])

        return res, i

    def generate_includes(self, i: int) -> str:
        res = ''
        for j in range(i, len(self.preprocessors)):
            if j > i:
                res += '<br />'
            incl = self.preprocessors[j][1]
            incl = self._substitute(incl[0]) + incl[1:-1] + self._substitute(incl[-1])
            res += include.format(incl)
        return res

    def _preparation(self):
        content, self.preprocessors = Helper.slice_content(self.body)
        i = int()
        while content[i][0] != Helper.oneline and content[i][0] != Helper.multiline and i < len(self.preprocessors):
            i += 1
        if content[i][0] == Helper.multiline:
            self.comment_list = [content[i]]
            del content[i]
        elif content[i][0] == Helper.oneline:
            comment_block = list()
            while content[i][0] == Helper.oneline and content[i][0] != Helper.multiline:
                comment_block.append(content[i])
                del content[i]

            self.comment_list = comment_block

        return content
