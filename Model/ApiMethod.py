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
        ret += str(re.sub(r"(\s)+",r"\1",str(self.description.strip()))) +"\n\n"
        ret += "Parameters: \n" + re.sub(r"(\s)+",r"\1",str(self.parameters.strip()))+"\n\n"
        ret += "Returns: \n" + re.sub(r"(\s)+",r"\1",str(self.returns.strip()))+"\n\n"
        return ret


    def attach_descriptions(self, tag):
        for string in tag.strings:
            if not re.search(r"^\s*$", string):
                self.description += str(re.sub(r",","", string)).strip() + " "

    def attach_parameters(self, tag):
        for string in tag.strings:
            if not re.search(r"^\s?$", string):
                self.parameters += str(re.sub(r",","", string)).strip() + " "
            self.parameters = re.sub(r"\n(\s)*", r"\n", self.parameters)
        if self.parameters != "":
            self.parameters += "|||\n"

    def attach_returns(self, tag):
        for string in tag.strings:
            if not re.search(r"^\s?$", string):
                self.returns += str(re.sub(r",","", string)).strip() + " "
        if self.returns != "":
            self.returns += "|||\n"