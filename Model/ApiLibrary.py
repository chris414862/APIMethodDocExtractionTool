import re


class ApiLibrary:
    '''This class represents a class in the API documentation'''
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.packages = []


    def set_library_name(self, url):
        self.name =  re.sub(r".*reference/(.*packages)", r"\1", url)

    def string(self):
        ret = ""
        for package in self.packages:
            ret += str(package.string()) + "\n\n"
        return ret
