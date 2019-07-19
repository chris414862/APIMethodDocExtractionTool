import re
from bs4 import Tag

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


def class_name_from_url(url):
    return re.sub(r".*/([^/]*)\.html", r"\1", url)
