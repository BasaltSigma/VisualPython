from node_map import Node, ConstantNode


class PrintNode(Node):

    def __init__(self, x, y):
        super().__init__("Print", Node.DEFAULT_FUNCTION_NODE, x, y)
        self.inputs.append((Node.EXEC_TYPE, "Exec"))
        self.inputs.append((Node.WILDCARD_TYPE, "Object to Print"))
        self.outputs.append((Node.EXEC_TYPE, "Exec"))

    def behaviour(self, input_list):
        print(input_list[0])


class StartNode(Node):

    def __init__(self, x, y):
        super().__init__("Start Program", Node.CONTROL_FLOW_NODE, x, y)
        self.outputs.append((Node.EXEC_TYPE, "Start"))

    def behaviour(self, input_list):
        pass


class IfElseNode(Node):

    def __init__(self, x, y):
        super().__init__("Branch", Node.CONTROL_FLOW_NODE, x, y)
        self.inputs.append((Node.EXEC_TYPE, "Exec"))
        self.inputs.append((Node.BOOL_TYPE, "Condition"))
        self.outputs.append((Node.EXEC_TYPE, "True"))
        self.outputs.append((Node.EXEC_TYPE, "False"))

    def behaviour(self, input_list: list):
        pass


class BooleanAndNode(Node):

    def __init__(self, x, y):
        super().__init__("Boolean AND", Node.MATHEMATICAL_NODE, x, y)
        self.inputs.append((Node.BOOL_TYPE, "A"))
        self.inputs.append((Node.BOOL_TYPE, "B"))
        self.outputs.append((Node.BOOL_TYPE, "Result"))

    def behaviour(self, input_list: list):
        return input_list[0] and input_list[1]


class BooleanOrNode(Node):

    def __init__(self, x, y):
        super().__init__("Boolean OR", Node.MATHEMATICAL_NODE, x, y)
        self.inputs.append((Node.BOOL_TYPE, "A"))
        self.inputs.append((Node.BOOL_TYPE, "B"))
        self.outputs.append((Node.BOOL_TYPE, "Result"))

    def behaviour(self, input_list: list):
        return input_list[0] or input_list[1]


class BooleanNotNode(Node):

    def __init__(self, x, y):
        super().__init__("Boolean NOT", Node.MATHEMATICAL_NODE, x, y)
        self.inputs.append((Node.BOOL_TYPE, "Input"))
        self.outputs.append((Node.BOOL_TYPE, "Result"))

    def behaviour(self, input_list: list):
        return not input_list[0]


class BooleanXorNode(Node):

    def __init__(self, x, y):
        super().__init__("Boolean XOR", Node.MATHEMATICAL_NODE, x, y)
        self.inputs.append((Node.BOOL_TYPE, "A"))
        self.inputs.append((Node.BOOL_TYPE, "B"))
        self.outputs.append((Node.BOOL_TYPE, "Result"))

    def behaviour(self, input_list: list):
        return (input_list[0] or input_list[1]) and not (input_list[0] and input_list[1])

class ConstantIntNode(ConstantNode):

    def __init__(self, x, y):
        super().__init__("Constant Integer", x, y, 0, Node.INTEGER_TYPE)


class ConstantStringNode(ConstantNode):

    def __init__(self, x, y):
        super().__init__("Constant String", x, y, "", Node.STRING_TYPE)


class ConstantFloatNode(ConstantNode):

    def __init__(self, x, y):
        super().__init__("Constant Float", x, y, 0.0, Node.FLOAT_TYPE)


class ConstantBoolNode(ConstantNode):

    def __init__(self, x, y):
        super().__init__("Constant Boolean", x, y, False, Node.BOOL_TYPE)