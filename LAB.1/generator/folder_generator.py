from . import Generator, FileGenerator
from .generator import active_page, prev_page
import os

content = ('''    <title>{}</title>
  </head>
  <body>
    <header class="pt-3 pb-1 container-fluid  bg-dark">
      <div class="h1 mx-auto d-flex justify-content-center" >
        <ol class="breadcrumb">
          {}
        </ol>
      </div>
    </header>
    <div class="pt-3 pb-3 container-fluid bg-secondary">
      <div class="container">
        <div class="bg-light">
          <ol class="p-3 h2">
            {}
          </ol>
        </div>
      </div>
    </div>''')
file_item = '<ul><a href="{}" class="text-dark">{}</a></ul>{}'
index_item = '<ul><a href="{}" class="text-dark"><span><span class="text-namespaces">{}</span>{}</span></a></ul>{}'


class FolderGenerator(Generator):

    @Generator.path_normaliser
    def __init__(self, output_path: str, outer_path: str, inner_path: str = ''):
        super().__init__(output_path, outer_path, inner_path)
        self.generators = list()

    def generate(self, include_dirs: bool = False):
        folders = list(os.walk(os.path.join(self.outer_path, self.inner_path)))
        r, d, f = folders[0]
        if include_dirs:
            for directory in d:
                self.generators.append(FolderGenerator(self.output_path, self.outer_path, os.path.join(self.inner_path,
                                                                                                       directory)))
        for file in f:
            if '.h' in file or '.cpp' in file:
                self.generators.append(FileGenerator(self.output_path, self.outer_path, os.path.join(self.inner_path,
                                                                                                     file)))

        for generator in self.generators:
            if type(generator) is FileGenerator:
                generator.generate()
            else:
                generator.generate(include_dirs)

        inp_file = open(os.path.join(self._templates_path, 'template.html'), 'r')
        template = inp_file.read().split('{content}', 1)
        inp_file.close()

        template.insert(1, content.format(self.name, self._generate_header(),
                                          self._generate_content_table()))

        self._generate_fs_tree()

        output = open(os.path.join(self.output_path, ('', self.inner_path)[include_dirs], 'content.html'), 'w')
        output.write(''.join(template))
        output.close()

    def _generate_header(self, current_path: str = '', increment_path: str = os.pardir + os.sep) -> str:
        res = super()._generate_header(current_path, increment_path)
        if self.name != os.path.basename(self.outer_path):
            return res.format(prev_page.format('', current_path + increment_path + 'content.html', os.path.basename(self.outer_path)))
        else:
            return res.format('')

    def _generate_content_table(self) -> str:
        res = '{}'
        for generator in self.generators:
            if type(generator) is FileGenerator:
                res = res.format(file_item.format(generator.name + '.html', generator.name, '{}'))
            else:
                res = res.format(file_item.format(os.path.join(generator.name, 'content.html'), generator.name, '{}'))

        return res.format('')

    def extract_index(self) -> list:
        res = list()
        for x in self.generators:
            res += x.extract_index()
        return res

    def generate_index(self) -> str:
        names = sorted(self.extract_index(), key=lambda element: (element[0], element[1]))
        res = '{}'
        for x in names:
            res = res.format(index_item.format(x[2] + '.html', x[0], x[1], '{}'))
        return res.format('')
