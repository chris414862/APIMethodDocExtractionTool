import re


class ApiPackage:
    '''This class represents a class in the API documentation'''
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.classes = []
        self.number_of_class_urls = 0
        self.bad_class_reads = list()

    def set_package_name(self, url):
        self.name = re.sub(r".*/([^/]*)/package-summary.html", r"\1", url)

    def string(self):
        ret = ""
        ret += "@@@\n" + str(self.name) + "\n@@@\n"
        for api_class in self.classes:
            ret += str(api_class.string().strip())+"\n\n"
        return ret