import re


class ApiPackage:
    '''This class represents a class in the API documentation'''
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.classes = []
        self.number_of_class_urls = 0
        self.bad_class_reads = list()

    def set_package_name(self, url, library_name):
        library_name = re.sub(r"\.", "/", library_name)
        regex = r".*reference/"+ re.escape(library_name.strip()) +"/(.*)package-summary.*"
        self.name = re.sub(regex, r"\1", url)
        # print(self.name)
        if self.name == url:
            self.name = re.sub(r".*reference/(.*)package-summary.*", r"\1", url)
        self.name = re.sub(r"[\\/]", ".", self.name)

        if self.name == "":
            self.name = "android"
        self.name = self.name.strip(".")

    def set_package_descrip(self,descrip):
        self.description = descrip

    def string(self):
        ret = ""
        ret += "@@@\n" + str(self.name) + "\n@@@\n"
        ret += self.description
        for api_class in self.classes:
            ret += str(api_class.string().strip())+"\n\n"
        return ret