import re


class ApiPackage:
    '''This class represents a class in the API documentation'''
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.classes = []

    def set_package_name(self, url):
        # print("package regex:")
        # print(re.sub(r"/([^/]*)/package-summary.html", r"\1", url))
        self.name = re.sub(r".*/([^/]*)/package-summary.html", r"\1", url)