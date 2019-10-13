import abstract as abstract
from jinja2 import Environment, FileSystemLoader


class Generator:
    def __init__(self):
        self.environment = Environment(loader=FileSystemLoader("templates"), trim_blocks=True)

    def generate(self):
        pass
