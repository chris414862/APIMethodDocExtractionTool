import re
from bs4 import Tag

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

    def attach_descriptions(self, tag):
        if "class" in tag.attrs and tag["class"] == ["caution"]:
            tag = tag.find_next_sibling("p")
        if isinstance(tag, Tag):# and tag.descendants is not None:
            # for descendant in tag.descendants:
            #     if isinstance(descendant,Tag) and (tag.name == "div" or tag.name == "h2"):
            #         return
                if tag.strings is not None:
                    for string in tag.strings:
                        if not re.search(r"^\s*$", string):

                            self.description += str(re.sub(r",","", string)) + " "

        for sibling in tag.next_siblings:
            if isinstance(sibling,Tag) and "class" in sibling.attrs and sibling["class"] == ["caution"]:
                continue
            # if self.name == "AccessibilityService":
            #     print(tag.prettify())
            #     print(self.name)
            #     print("###################")

            # if self.name =="PreferenceFragment":

            if sibling.name == "div" or sibling.name == "h2":
                return

            # for descendant in tag.descendants:
            #     if isinstance(descendant,Tag) and (tag.name == "div" or tag.name == "h2"):
            #         return

            if isinstance(sibling, Tag) and sibling.strings is not None:
                for string in sibling.strings:
                    if string.parent.name == "div" or string.parent.name == "h2":
                        return
                    if not re.search(r"^\s*$", string):
                        self.description += str(re.sub(r",","", string))+" "


        # for string in tag.next_siblings:
        #     if re.search(r"Summary[ \n]?", string):
        #         break
        #     if not re.search(r"^\s*$", string):
        #         self.description += string.strip() + " "

    def string(self):
        ret = ""
        ret += "@@@\n" + str(self.name) + "\n@@@\n"
        ret += self.description
        for api_class in self.classes:
            ret += str(api_class.string().strip())+"\n\n"
        return ret