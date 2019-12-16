import os

active_page = '{}<li class="breadcrumb-item active" aria-current="page">{}</li>'
prev_page = '{}<li class="breadcrumb-item"><a class="text-light" href="{}">{}</a></li>'


class Generator:
    _templates_path = os.path.normpath("./templates")

    def __init__(self, output_path: str, outer_path: str, inner_path: str):
        self.output_path = output_path
        self.outer_path = outer_path
        self.inner_path = inner_path
        self.name = os.path.basename(inner_path)
        if self.name == '':
            self.name = os.path.basename(self.outer_path)

    def generate(self, include_folders: bool):
        pass

    @staticmethod
    def path_normaliser(func):
        def wrapper(self, output_path, outer_path, inner_path=''):
            output_path = os.path.normpath(output_path)
            outer_path = os.path.normpath(outer_path)
            if inner_path != '':
                inner_path = os.path.normpath(inner_path)
            func(self, output_path, outer_path, inner_path)

        return wrapper

    def _generate_fs_tree(self):
        path = self.inner_path.split(os.sep)
        folder = self.output_path
        if not os.path.isdir(folder):
            os.mkdir(folder)
        for i in range(0, len(path) - 1):
            folder = os.path.join(folder, path[i])
            if not os.path.isdir(folder):
                os.mkdir(folder)

    def _generate_header(self, current_path: str = '', increment_path: str = os.pardir + os.sep) -> str:
        path = self.inner_path.split(os.sep)
        res = active_page.format('{}', self.name)
        for i in range(len(path) - 2, -1, -1):
            res = res.format(prev_page.format('{}', current_path + 'content.html', path[i]))
            current_path += increment_path
        return res

    def extract_index(self):
        pass
