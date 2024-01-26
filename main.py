import pparser, lex, generator_code, Symantic

f = open('lex.txt')
lol = lex.Lexer(f)
i = 0
# while (lol.get_next_token().__str__().find("EOF")) == -1:
#     print(lol.get_next_token())
pars = pparser.Parser(lol)
# print(pars.parse())
gen = generator_code.Gen(pars)
gen.fullGenerate()
