import os


class Function:
    def __init__(self, path, name, line, class_name=None):
        self.__path = os.path.basename(path)
        self.line = line
        self.class_name = class_name
        self.comment = str()

        parts = name.split("(", 1)
        type_name = parts[0].split()
        self.params = " ".join(parts[1:])[0:-1]

        if len(type_name) >= 2:
            self.ret_type = type_name[0]
            self.name = type_name[1]
        elif len(type_name) == 1:
            self.ret_type = None
            self.name = type_name[0]

    @property
    def is_operator(self) -> bool:
        return self.name.startswith("operator")

    @property
    def is_constructor(self) -> bool:
        return self.ret_type is None

    @property
    def is_method(self) -> bool:
        return self.class_name is not None

    @property
    def kind(self):
        if self.is_constructor:
            return "Constructor"
        elif self.is_method:
            return "Method"
        else:
            return "Function"

    @property
    def path(self):
        if self.is_method:
            return self.__path + ":" + self.class_name
        else:
            return self.__path
