import re


class ApiClass:
    '''This class represents a class in the API documentation'''
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.methods = []

    def string(self):
        ret = "###\n"+str(self.name)+"\n###\n"
        ret += str(re.sub(r"(\s)+",r"\1",str(self.description.strip())))+"\n"
        for method in self.methods:
            ret += str(method.string().strip())+"\n\n"

        return ret

    def attach_descriptions(self, tag):
        for string in tag.strings:
            if re.search(r"Summary[ \n]?", string):
                break
            if not re.search(r"^\s*$", string):
                self.description += string.strip()


def class_name_from_url(url):
    return re.sub(r".*/([^/]*)\.html", r"\1", url)
