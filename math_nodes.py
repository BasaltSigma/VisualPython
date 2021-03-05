from node_map import Node


class FloatAddNode(Node):

    def __init__(self, x, y):
        super().__init__("Add Float", Node.MATHEMATICAL_NODE, x, y)
        self.inputs.append((Node.FLOAT_TYPE, "A"))
        self.inputs.append((Node.FLOAT_TYPE, "B"))
        self.outputs.append((Node.FLOAT_TYPE, "Result"))

    def behaviour(self, input_list: list):
        return input_list[0] + input_list[1]


class FloatSubtractNode(Node):

    def __init__(self, x, y):
        super().__init__("Subtract Float", Node.MATHEMATICAL_NODE, x, y)
        self.inputs.append((Node.FLOAT_TYPE, "A"))
        self.inputs.append((Node.FLOAT_TYPE, "B"))
        self.outputs.append((Node.FLOAT_TYPE, "Result"))

    def behaviour(self, input_list: list):
        return input_list[0] - input_list[1]


class FloatMultiplyNode(Node):

    def __init__(self, x, y):
        super().__init__("Multiply Float", Node.MATHEMATICAL_NODE, x, y)
        self.inputs.append((Node.FLOAT_TYPE, "A"))
        self.inputs.append((Node.FLOAT_TYPE, "B"))
        self.outputs.append((Node.FLOAT_TYPE, "Result"))

    def behaviour(self, input_list: list):
        return input_list[0] * input_list[1]