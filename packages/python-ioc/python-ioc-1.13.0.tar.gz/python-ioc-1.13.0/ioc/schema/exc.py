

class InvalidDeclaration(Exception):

    def __init__(self, dep, message):
        self.dep = dep
        self.message = message
