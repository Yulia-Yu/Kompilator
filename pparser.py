import sys
from lex import Lexer, Token
from Symantic import SymTable


class Node:
    gen = ' '
    def __get_class_name(self):
        c = str(self.__class__)
        pos_1 = c.find('.') + 1
        pos_2 = c.find("'", pos_1)
        return f"{c[pos_1:pos_2]}"

    def __repr__(self, level=0):
        attrs = self.__dict__  # словарь атрибут : значение
        # если атрибут один и тип его значения - это список,
        # то это узел некоторой последовательности (подпрограмма, либо список)
        if len(attrs) == 1 and isinstance(list(attrs.values())[0], list):
            is_sequence = True
        else:
            is_sequence = False
        res = f"{self.__get_class_name()}\n"
        if is_sequence:
            elements = list(attrs.values())[0]
            for el in elements:
                res += '|   ' * level
                res += "|+-"
                res += el.__repr__(level + 1)
        else:
            for attr_name in attrs:
                res += '|   ' * level
                res += "|+-"
                if isinstance(attrs[attr_name], Token):
                    res += f"{attr_name}: {attrs[attr_name]}\n"
                else:
                    res += f"{attr_name}: {attrs[attr_name].__repr__(level + 1)}"
        return res



class NodeProgram(Node):
    def __init__(self, children):
        self.children = children

    def generate(self):
        code = ""
        for child in self.children:
            code += f"    {child.generate()}\n"
        return code


class NodeBlock(NodeProgram):
    def __init__(self, tokens):
        self.tokens = tokens
        self.value = ""
        for i in self.tokens:
            self.value += i.value + "\n        "
    pass


class NodeElseBlock(NodeBlock):
    pass


class NodeDeclaration(Node):
    def __init__(self, _type, id):
        self.type = _type
        self.id = id

    def generate(self):
        code = self.id
        for child in self.children:
            code += f"{child.generate()};\n"
        return code

class NodeAssigning(Node):
    def __init__(self, left_side, right_side):
        if left_side == 'Ukk' or right_side == 'Ukk':
            print('Переменная не объявлена')
        else:
            self.left_side = left_side
            self.right_side = right_side
            self.value = self.left_side.id.value + " = " + self.right_side.value.value
    def generate(self):
        code = self.left_side.id.value + " = "
        code += self.right_side.value.value
        return code

class NodeFunction(Node):
    def __init__(self, ret_type, id, formal_params, block):
        self.ret_type = ret_type
        self.id = id
        self.formal_params = formal_params
        self.block = block

        def generate(self):
            code = "void " + self.id + "(" + self.formal_params + ")" + "{" + self.block + "}"
            for child in self.children:
                code += f"{child.generate()};\n"
            return code


class NodeSequence(Node):
    def __init__(self, members):
        self.members = members


class NodeParams(Node):
    def __init__(self, params):
        self.params = params



class NodeFormalParams(NodeParams):
    pass


class NodeActualParams(NodeParams):
    pass

class NodeLeftSkobka(Node):
    pass
class NodeIfConstruction(Node):
    def __init__(self, condition, block, else_block):
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def generate(self):
        code = "if " + "(" + self.condition.value.value + "):\n" + "        " + self.block.value
        if (self.else_block.value):
            code += "\n    else:\n" + "        " + self.else_block.value
        return code


class NodeWhileConstruction(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def generate(self):
        code = "while " + "(" + self.condition + ")" + "{" + self.block + "}"
        for child in self.children:
            code += f"{child.generate()};\n"
        return code

class NodeReturnStatement(Node):
    def __init__(self, expression):
        self.expression = expression
    def generate(self):
        code = "return " + self.expression
        for child in self.children:
            code += f"{child.generate()};\n"
        return code

class NodeLiteral(Node):
    def __init__(self, value):
        self.value = value
    def generate(self):
        code = self.value
        return code

class NodeStringLiteral(NodeLiteral): pass


class NodeIntLiteral(NodeLiteral):
    def __init__(self, value):
        super().__init__(value)



class NodeFloatLiteral(NodeLiteral): pass


class NodeVar(Node):
    def __init__(self, id):
        self.id = id
        self.value = id
    def generate(self):
        code = self.id
        return code


class NodeAtomType(Node):
    def __init__(self, id):
        self.id = id
    def generate(self):
        code = self.id
        for child in self.children:
            code += f"{child.generate()};\n"
        return code

class NodeComplexType(Node):
    def __init__(self, id, size):
        self.id = id
        self.size = size


class NodeFunctionCall(Node):
    def __init__(self, id, actual_params):
        self.id = id
        self.actual_params = actual_params
    def generate(self):
        code = self.id + "(" + self.actual_params + ")"
        for child in self.children:
            code += f"{child.generate()};\n"
        return code

class NodeIndexAccess(Node):
    def __init__(self, var, index):
        self.var = var
        self.index = index


class NodeUnaryOperator(Node):

    def generate(self):
        code = self.operand
        for child in self.children:
            code += f"{child.generate()};\n"
        return code


class NodeUnaryMinus(NodeUnaryOperator):
    def __init__(self, operand):
        self.operand = operand
        self.operand.value.value = "-" + operand.value.value
        self.value = self.operand.value
    pass


class NodeNot(NodeUnaryOperator):

    pass


class NodeBinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class NodeL(NodeBinaryOperator):
    pass


class NodeG(NodeBinaryOperator):
    pass


class NodeLE(NodeBinaryOperator):
    pass


class NodeGE(NodeBinaryOperator):
    pass


class NodeEQ(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = self.left.value.value + " == " + self.right.value.value
        self.value = left.value
    pass


class NodeNEQ(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = "not (" + self.left.value.value + " == " + self.right.value.value + ")"
        self.value = left.value


class NodeOr(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = self.left.value.value + " or " + self.right.value.value
        self.value = left.value
    pass


class NodeAnd(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = self.left.value.value + " and " + self.right.value.value
        self.value = left.value
    pass


class NodePlus(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = self.left.value.value + " + " + self.right.value.value
        self.value = left.value



class NodeMinus(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = self.left.value.value + " - " + self.right.value.value
        self.value = left.value
    pass


class NodeDivision(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = self.left.value.value + " / " + self.right.value.value
        self.value = left.value
    pass


class NodeMultiply(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = self.left.value.value + " * " + self.right.value.value
        self.value = left.value



class NodeIDivision(NodeBinaryOperator):

    pass


class NodeMod(NodeBinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right
        self.left.value.value = self.left.value.value + " % " + self.right.value.value
        self.value = left.value
    pass

s_table = SymTable()

class Parser:
    def __init__(self, lexer: Lexer):
        #self.s_table = SymTable()
        self.lexer = lexer
        self.token = self.lexer.get_next_token()

    def next_token(self):
        self.token = self.lexer.get_next_token()

    def require(self, expected_token_name):
        if self.token.name != expected_token_name:
            self.error(f"Ожидается токен {Token.token_names[expected_token_name]}!")

    def error(self, msg):
        print(f'Ошибка синтаксического анализа ({self.lexer.lineno}, {self.lexer.pos}): {msg}')
        sys.exit(1)

    def block(self) -> Node:
        statements = []
        while self.token.name not in {Token.RCBR, Token.EOF}:
            statements.append(self.statement())
            self.require(Token.SEMI)
            self.next_token()
        return NodeBlock(statements)

    def else_block(self) -> Node:
        statements = []
        while self.token.name not in {Token.RCBR, Token.EOF}:
            statements.append(self.statement())
            self.require(Token.SEMI)
            self.next_token()
        return NodeElseBlock(statements)

    def actual_params(self) -> Node:
        params = []
        while self.token.name not in {Token.RBR, Token.EOF}:
            params.append(self.expression())
            if self.token.name == Token.COMMA:
                self.next_token()
        return NodeActualParams(params)

    def formal_params(self) -> Node:
        params = []
        while self.token.name not in {Token.RBR, Token.EOF}:
            params.append(self.declaration())
            if self.token.name == Token.COMMA:
                self.next_token()
        return NodeFormalParams(params)

    def operand(self) -> Node:
        first_token = self.token

        if self.token.name == Token.STRING_LITERAL:
            self.next_token()
            return NodeStringLiteral(first_token)
        if self.token.name == Token.INT_LITERAL:
            self.next_token()
            return NodeIntLiteral(first_token)
        if self.token.name == Token.ID:
            if not s_table.check(first_token.value):
                return 'Ukk'
            self.next_token()
            if self.token.name == Token.LBR:
                self.next_token()
                actual_params = self.actual_params()
                self.require(Token.RBR)
                self.next_token()
                return NodeFunctionCall(first_token, actual_params)
            if self.token.name == Token.LSBR:
                self.next_token()
                index = self.expression()
                self.require(Token.RSBR)
                self.next_token()
                return NodeIndexAccess(NodeVar(first_token), index)
            if self.token.name ==  Token.LBR:
                self.next_token()
                expression = self.expression()
                self.require(Token.RBR)
                self.next_token()
                return expression

            else:
                return NodeVar(first_token)

    def factor(self) -> Node:
        if self.token.name == Token.MINUS:
            self.next_token()
            return NodeUnaryMinus(self.operand())
        else:
            return self.operand()

    def term(self) -> Node:
        left = self.factor()
        op = self.token.name
        while op in {Token.ASTERISK, Token.SLASH, Token.DSLASH, Token.PERCENT}:
            self.next_token()
            if op == Token.ASTERISK:
                left = NodeMultiply(left, self.factor())
            if op == Token.SLASH:
                left = NodeDivision(left, self.factor())
            if op == Token.DSLASH:
                left = NodeIDivision(left, self.factor())
            if op == Token.PERCENT:
                left = NodeMod(left, self.factor())
            op = self.token.name
        return left

    def expression(self) -> Node:
        left = self.term()
        op = self.token.name
        while op in {Token.PLUS, Token.MINUS}:
            self.next_token()
            if op == Token.PLUS:
                left = NodePlus(left, self.term())
            if op == Token.MINUS:
                left = NodeMinus(left, self.term())
            op = self.token.name
        return left

    def logical_operand(self) -> Node:
        if self.token.name == Token.NOT:
            self.next_token()
            return NodeNot(self.logical_operand())
        if self.token.name == Token.LBR:
            self.next_token()
            condition = self.condition()
            self.require(Token.RBR)
            self.next_token()
            return condition
        else:
            return self.expression()

    def and_operand(self) -> Node:
        left = self.logical_operand()
        op = self.token.name
        while op in {Token.L, Token.G, Token.LE, Token.GE, Token.EQ, Token.NEQ}:
            self.next_token()
            if op == Token.L:
                left = NodeL(left, self.expression())
            if op == Token.G:
                left = NodeG(left, self.expression())
            if op == Token.LE:
                left = NodeLE(left, self.expression())
            if op == Token.GE:
                left = NodeGE(left, self.expression())
            if op == Token.EQ:
                left = NodeEQ(left, self.expression())
            if op == Token.NEQ:
                    left = NodeNEQ(left, self.expression())
            op = self.token.name
        return left

    def or_operand(self) -> Node:
        left = self.and_operand()
        op = self.token.name
        while op == Token.AND:
            self.next_token()
            left = NodeAnd(left, self.and_operand())
            op = self.token.name
        return left

    def condition(self) -> Node:
        left = self.or_operand()
        op = self.token.name
        while op == Token.OR:
            self.next_token()
            left = NodeOr(left, self.or_operand())
            op = self.token.name
        return left

    def type(self) -> Node:
        id = self.token
        self.next_token()
        if self.token.name != Token.LSBR:
            return NodeAtomType(id)
        self.next_token()
        self.require(Token.INT_LITERAL)
        size = self.token
        self.next_token()
        self.require(Token.RSBR)
        self.next_token()
        return NodeComplexType(id, size)

    def sequence(self) -> Node:
        members = []
        while self.token.name not in {Token.RSBR, Token.EOF}:
            members.append(self.expression())
            if self.token.name == Token.COMMA:
                self.next_token()
        return NodeSequence(members)

    def declaration(self) -> Node:
        self.require(Token.ID)
        _type = self.type()
        self.require(Token.ID)
        id = self.token
        self.next_token()
        return NodeDeclaration(_type, id)

    def statement(self) -> Node:
        # declaration | assigning | function-call
        if self.token.name == Token.DOL:
            self.next_token()
            s_table.Add(self.token.value)
        if self.token.name == Token.DOG:
            self.next_token()
            s_table.Add(self.token.value)
        if self.token.name == Token.ID:
            first_token = self.token
            self.next_token()
            if not s_table.check(first_token.value):
                self.error("Ожидалось объявление переменной, присваивание или вызов функции!")
                return 'Ukk'
            # например int abc
            if self.token.name == Token.ID:
                name = self.token
                self.next_token()
                return NodeDeclaration(NodeAtomType(first_token), name)
                # например int[10] abc
            if self.token.name == Token.LSBR:
                self.next_token()
                self.require(Token.INT_LITERAL)
                size = self.token
                self.next_token()
                self.require(Token.RSBR)
                self.next_token()
                self.require(Token.ID)
                name = self.token
                self.next_token()
                return NodeDeclaration(NodeComplexType(first_token, size), name)
            # например abc = 123 или abc = [1,2,3]
            if self.token.name == Token.ASSIGN:
                self.next_token()
                if self.token.name != Token.LSBR:
                    return NodeAssigning(NodeVar(first_token), self.expression())
                self.next_token()
                sequence = self.sequence()
                self.require(Token.RSBR)
                self.next_token()
                return NodeAssigning(NodeVar(first_token), sequence)
            # например abc(1,3,4)
            if self.token.name == Token.LBR:
                self.next_token()
                actual_params = self.actual_params()
                self.require(Token.RBR)
                self.next_token()
                return NodeFunctionCall(first_token, actual_params)
            else:
                 self.error("Ожидалось объявление переменной, присваивание или вызов функции!")

            # function
        if self.token.name == Token.SUB:
            # пропускаем токен SUB
            self.next_token()
            # следующий токен содержит тип возвр. значения. это ID типа.
            self.require(Token.ID)
            # сохраним тип
            first_token = self.type()
            # следующий токен содержит ID функции
            self.require(Token.ID)
            # сохраним имя функции
            name = self.token
            # смотрим на следующий токен
            self.next_token()
            # следующий токен ( - скобка перед формальными параметрами
            self.require(Token.LBR)
            # пропускаем скобку
            self.next_token()
            # начинаем разбор формальных параметров
            formal_params = self.formal_params()
            # после разбора формальных параметров лексер должен смотреть на закрывающую скобку )
            self.require(Token.RBR)
            # пропускаем скобку
            self.next_token()
            # следующий токен { - скобка перед телом функции
            self.require(Token.LCBR)
            # пропускаем скобку
            self.next_token()
            # начинаем разбирать тело
            block = self.block()
            # после разбора тела функции мы должны встретить закрывающую скобку }
            self.require(Token.RCBR)
            self.next_token()
            return NodeFunction(first_token, name, formal_params, block)

        if self.token.name == Token.IF:
            self.next_token()
            condition = self.condition()
            self.require(Token.LCBR)
            self.next_token()
            block = self.block()
            self.require(Token.RCBR)
            self.next_token()
            if self.token.name != Token.ELSE:
                # возврат условной конструкции без блока else
                return NodeIfConstruction(condition, block, NodeElseBlock([]))
            self.next_token()
            self.require(Token.LCBR)
            self.next_token()
            else_block = self.else_block()
            self.require(Token.RCBR)
            self.next_token()
            return NodeIfConstruction(condition, block, else_block)

        if self.token.name == Token.WHILE:
            self.next_token()
            condition = self.condition()
            self.require(Token.LCBR)
            self.next_token()
            block = self.block()
            self.require(Token.RCBR)
            self.next_token()
            return NodeWhileConstruction(condition, block)

        if self.token.name == Token.RETURN:
            self.next_token()
            expression = self.expression()
            return NodeReturnStatement(expression)

    def parse(self) -> Node:
        if self.token.name == Token.EOF:
            self.error("Пустой файл!")
        else:
            statements = []
            while self.token.name != Token.EOF:
                statements.append(self.statement())
                self.require(Token.SEMI)
                self.next_token()
            print(s_table.variables)
            return NodeProgram(statements)


