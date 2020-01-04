from datetime import datetime

from generator import Generator, FolderGenerator
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
          <div class="h1 border-bottom">
            Documentation for project: {}<br /><span class=" h2 text-info">Version: <i>1.0</i></span><br />
            <span class="h4">Generated: {} <br />by LAB.1 generator</span>
          </div>
          <div class="h3 text-center">
            Content: <a class="text-dark" href="content.html">{}</a><br />
            Index: <a class="text-dark" href="index.html">index</a><br />
          </div>
        </div>
      </div>
    </div>''')

index = ('''    <title>{}</title>
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


class ModuleGenerator(FolderGenerator):
    @Generator.path_normaliser
    def __init__(self, output_path, outer_path, *args):
        super().__init__(output_path, outer_path)

    def generate(self, include_dirs: bool = False):
        super().generate(include_dirs)
        inp_file = open(os.path.join(self._templates_path, 'template.html'), 'r')
        template = inp_file.read().split('{content}', 1)
        inp_file.close()

        curr_timestamp = datetime.today()
        template.insert(1, content.
                        format(self.name, self._generate_header(), self.name,
                               '.'.join([str(curr_timestamp.day), str(curr_timestamp.month), str(curr_timestamp.year)])
                               + ' ' + ':'.join([str(curr_timestamp.hour), str(curr_timestamp.minute),
                                                  str(curr_timestamp.second)]),
                               self.name))

        output = open(os.path.join(self.output_path, self.inner_path, 'project.html'), 'w')
        output.write(''.join(template))
        output.close()

        template[1] = index.format(self.name, self._generate_header(), self.generate_index())

        output = open(os.path.join(self.output_path, self.inner_path, 'index.html'), 'w')
        output.write(''.join(template))
        output.close()


class ProjectGenerator(ModuleGenerator):
    def generate(self, include_dirs: bool = True):
        super().generate(include_dirs)
