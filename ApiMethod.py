import re

class ApiMethod:
    '''This class represents a class in the API documentation'''
    def __init__(self, name="",descrip="", parameters="", returns=""):
        self.name = name
        self.description = descrip
        self.parameters = parameters
        self.returns = returns


    def string(self):
        ret = "---\n"+str(self.name)+"\n---\n"
        ret += str(self.description) +"\n\n"
        ret += "Parameters: \n" + str(self.parameters.strip())+"\n\n"
        ret += "Returns: \n" + str(self.returns.strip())+"\n\n"
        return ret


    def attach_descriptions(self, tag):
        for string in tag.strings:
            if not re.search(r"^\s*$", string):
                self.description += string.strip()

    def attach_parameters(self, tag):
        for string in tag.strings:
            if not re.search(r"^\s?$", string):
                self.parameters += string.strip() + " "
        if self.parameters != "":
            self.parameters += "|||\n"

    def attach_returns(self, tag):
        for string in tag.strings:
            if not re.search(r"^\s?$", string):
                self.returns += string.strip() + " "
        if self.returns != "":
            self.returns += "|||\n"