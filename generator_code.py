import pparser as p

class Gen:
    def __init__(self):
        self.code = ""

    def declaration_part(self, dp):
        return ""

    def if_type(self, node):
        c = ""
        if node.type == "NodeVariable":
            c += f'"{node.value}"'
        else: c += f"{node.value}"
        return c

    def condition(self, node):
        if_type = self.if_type(node.left)
        c = f"{if_type}"
        if_type = self.if_type(node.rigth)
        if node.type == "NodeEqualOperator":
            c += f"== {if_type}"
        elif node.type == "NodeNotEqualOperator":
            c += f"!= {if_type}"
        elif node.type == "NodeGreaterOperator":
            c += f"> {if_type}"
        elif node.type == "NodeSmallerOperator":
            c += f"< {if_type}"

        return c

    def if_operation(self, node):
        c = ""
        if node.type == "NodePlusOperator":
            c += " + "
        elif node.type == "NodeMinusOperator":
            c += " - "
        elif node.type == "NodeMultiplyOperator":
            c += " * "
        elif node.type == "NodeDivideOperator":
            c += " / "

        if_type = self.if_type(self, node.left)
        c += f"{if_type}"

        return c

    def assign_operation(self, node):
        c = f"{node.left.value} = "
        cond = node.right.type != "NodeNumber" or node.right.type != "NodeVariable"

        if not cond:
            if_type = self.if_type(node.right)
            c += f"{if_type}"
        while cond:
            if_type = self.if_type(node.left)
            c += f"{if_type}"

            if_operation = self.if_operation(node.rigth)
            c += f"{if_operation}"

        c += ";\n"
        return c

    def if_condition(self, node):
        condition = self.condition(node.condition)
        c = f"if ({condition})"+" {\n"
        node = node.block.statement_part
        # как вставить statement_part

        c += "}\n"
        return c

    def while_repetitive_statement(self, node):
        condition = self.condition(node.condition)
        c = f"while ({condition})"+" {\n"
        node = node.block.statement_part
        # как вставить statement_part

        c += "}\n"
        return c


    def statement_part(self, sp):
        c = ""
        for i in sp:
            if (isinstance(i, p.NodeAssignOperation)):
                assign_operation = self.assign_operation(i)
                c += f"{assign_operation}"
            if (isinstance(i, p.NodeIfCondition)):
                if_condition = self.if_condition(i)
                c += f"{if_condition}"
            if (isinstance(i, p.NodeWhileRepetitieStatement)):
                while_repetitive_statement = self.while_repetitive_statement(i)
                c += f"{while_repetitive_statement}"

        return c

    def generate(self, parser : p.NodeProgram):
        self.code = ""

        self.code += "int main(){\n"
        statement_part = self.statement_part(parser.statememt)
        self.code += f"{statement_part}"

        self.code += "   return 0;\n}"