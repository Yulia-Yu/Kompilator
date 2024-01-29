
from lex import Lexer, Token
from pparser import Parser, NodeProgram
from generator_code import Gen

from Symantic import SymTable

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = open("input.txt", 'r')
    lex = Lexer(f)
    #t = lex.get_next_token()
    #while t.name != Token.EOF:
    #    print(t)
    #    t = lex.get_next_token()
    #print(t)
    #f.close()
    pars = Parser(Lexer(f))
    gen = Gen(pars)
    #print(pars.parse())
    #print(pars.gen())

    gen.fullGenerate()

    f.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
