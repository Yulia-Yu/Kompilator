from collections import OrderedDict

class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymTable:
    #data: OrderedDict[str, Symbol]
    def __init__(self):
        self.variables = OrderedDict()


    def Add(self, symbol):
        self.variables[symbol.name] = symbol
    #def Get(self, variable) -> Symbol: pass

    def check(self, name):
        return name in self.variables

    def update_type(self, name, new_type):
        if name in self.variables:
            self.variables[name].type = new_type

    def get_type(self, name):
        return self.variables[name].type


