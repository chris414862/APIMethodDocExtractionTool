

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
        ret += "Parameters: \n" + str(self.parameters)+"\n\n"
        ret += "Returns: \n" + str(self.returns)+"\n\n"
        return ret