from node_map import Node


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


class ConstantNode(Node):

    def __init__(self, display_name, x, y, value, val_type):
        super().__init__(display_name, Node.VARIABLE_NODE, x, y)
        self.val_type = val_type
        self.val = value
        self.outputs.append((val_type, "Value"))

    def behaviour(self, input_list: list):
        return self.val


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