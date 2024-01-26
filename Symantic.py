class Symbol:
    name: str
    type: str

class SymTable:
    #data: OrderedDict[str, Symbol]
    def __init__(self):
        self.variables = []
    def Add(self, name):
        self.variables.append(name)
    #def Get(self, variable) -> Symbol: pass
    def check(self, variable):
        return variable in self.variables



