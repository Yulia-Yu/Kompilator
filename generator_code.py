import sys
from pparser import Parser
import pparser as p


class Gen:
    def __init__(self, parser: Parser):
        self.pars = parser

    def gen(self) -> str:
        if self.pars.token.name == p.Token.EOF:
            self.pars.error("Пустой файл!")
        else:
            statements = []
            while self.pars.token.name != p.Token.EOF:
                statements.append(self.pars.statement())
                self.pars.require(p.Token.SEMI)
                self.pars.next_token()
            return p.NodeProgram(statements).generate()

    def fullGenerate(self):
        print("if __name__ == '__main__':")
        print(self.gen())


