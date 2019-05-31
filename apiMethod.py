

class apiMethod:
    '''This class represents a class in the API documentation'''
    def __init__(self, name="",descrip=""):
        self.name = name
        self.description = descrip


    def string(self):
        ret = "---\n"+str(self.name)+"\n---\n"
        ret += str(self.description) +"\n"
        return ret