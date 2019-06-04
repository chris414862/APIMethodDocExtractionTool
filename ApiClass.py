import re


class ApiClass:
    '''This class represents a class in the API documentation'''
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.methods = []

    def string(self):
        ret = "###\n"+str(self.name)+"\n###\n"
        ret += str(self.description)+"\n"
        for method in self.methods:
            ret += str(method.string().strip())+"\n"

        return ret

    def attach_descriptions(self, tag):
        for string in tag.strings:
            if not re.search(r"^\s*$", string):
                self.description += string.strip()