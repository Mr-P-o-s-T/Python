from .generator import Generator, prev_page, active_page
from data.file_parser import FileParser
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
      <div class="p-3 container text-comment bg-light">
        {}
      </div>
      <h2 class="text-white border-bottom">Defines:</h2>
      <div class="p-3 container bg-light">
        {}
      </div>
    </div>
    <div class="container">
      <h2 class="text-white border-bottom">Includes:</h2>
        <div class="p-3 container bg-light">
          {}
        </div>
      </div>
    <div class="container">
      <h2 class="text-white border-bottom">Classes:</h2>
      <div class="p-3 container bg-light">
        {}
      </div>
    </div>
    <div class="container">
      <h2 class="text-white border-bottom">Functions:</h2>
      <div class="p-3 container bg-light">
        {}
      </div>
    </div>
    <div class="container">
      <h2 class="text-white border-bottom">Variables:</h2>
      <div class="p-3 container bg-light">
        {}
      </div>
    </div>
  </div>''')


class FileGenerator(Generator):
    @Generator.path_normaliser
    def __init__(self, output_path: str, outer_path: str, inner_path: str = ''):
        super().__init__(output_path, outer_path, inner_path)
        if inner_path == '':
            self.parser = FileParser(os.path.join(self.outer_path))
        else:
            self.parser = FileParser(os.path.join(self.outer_path, self.inner_path))

    def generate(self, *args, **kwargs):
        print(os.path.join(self.outer_path, self.inner_path))
        try:
            self.parser.parse()
        except Exception as e:
            print('Parsing failed!')
            self.parser = None
            return
        inp_file = open(os.path.join(self._templates_path, 'template.html'), 'r')
        template = inp_file.read().split('{content}', 1)
        inp_file.close()

        defines, i = self.parser.generate_defines()

        template.insert(1, content.format(self.name, self._generate_header(), self.parser.comment_list,
                                          defines, self.parser.generate_includes(i), self.parser.generate_classes()[0],
                                          self.parser.generate_functions(), self.parser.generate_variables()))

        self._generate_fs_tree()
        output = open(os.path.join(self.output_path, (self.inner_path, self.name)[self.inner_path == '']) + '.html', 'w')
        output.write(''.join(template))
        output.close()

    def _generate_header(self, current_path: str = '', increment_path: str = os.pardir + os.sep) -> str:
        res = super()._generate_header(current_path, increment_path)
        if self.name != os.path.basename(self.outer_path):
            return res.format(prev_page.format('', current_path + increment_path + 'content.html',
                                               os.path.basename(self.outer_path)))
        else:
            return res.format('')

    def extract_index(self):
        if self.parser is not None:
            res = self.parser.generate_index()
            for i in range(len(res)):
                res[i] = res[i] + (self.inner_path, )
            return res
        return []

