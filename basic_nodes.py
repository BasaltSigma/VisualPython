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


class ForEachLoopListNode(Node):

    def __init__(self, x, y):
        super().__init__("Foreach", Node.CONTROL_FLOW_NODE, x, y)
        self.inputs.append((Node.EXEC_TYPE, "Entry"))
        self.inputs.append((Node.LIST_TYPE, "List"))
        self.outputs.append((Node.EXEC_TYPE, "Loop Body"))
        self.outputs.append((Node.INTEGER_TYPE, "Index"))
        self.outputs.append((Node.EXEC_TYPE, "Completed"))

    def behaviour(self, input_list: list):
        pass


class WhileLoopNode(Node):

    def __init__(self, x, y):
        super().__init__("While Loop", Node.CONTROL_FLOW_NODE, x, y)
        self.inputs.append((Node.EXEC_TYPE, "Entry"))
        self.inputs.append((Node.BOOL_TYPE, "Condition"))
        self.outputs.append((Node.EXEC_TYPE, "Loop Body"))
        self.outputs.append((Node.EXEC_TYPE, "Completed"))

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


class OpenTextFileNode(Node):

    def __init__(self, x, y):
        super().__init__("Open Text File", Node.DEFAULT_FUNCTION_NODE, x, y)
        self.inputs.append((Node.EXEC_TYPE, "Exec"))
        self.inputs.append((Node.STRING_TYPE, "File Path"))
        self.outputs.append((Node.EXEC_TYPE, "Exec"))
        self.outputs.append((Node.LIST_TYPE, "Lines"))

    def behaviour(self, input_list: list):
        lines = []
        with open(input_list[0], "r") as my_file:
            while my_file.readable():
                lines.append(my_file.readline())
        return lines


class ListGetAtIndexNode(Node):

    def __init__(self, x, y):
        super().__init__("Get At Index", Node.COLLECTION_NODE, x, y)
        self.inputs.append((Node.LIST_TYPE, "List"))
        self.inputs.append((Node.INTEGER_TYPE, "Index"))
        self.outputs.append((Node.WILDCARD_TYPE, "Value"))

    def behaviour(self, input_list: list):
        return input_list[0][input_list[1]]


class ListAppendNode(Node):

    def __init__(self, x, y):
        super().__init__("Append", Node.COLLECTION_NODE, x, y)
        self.inputs.append((Node.EXEC_TYPE, "Exec"))
        self.inputs.append((Node.LIST_TYPE, "Input List"))
        self.inputs.append((Node.WILDCARD_TYPE, "Item"))
        self.outputs.append((Node.EXEC_TYPE, "Exec"))
        self.outputs.append((Node.LIST_TYPE, "Result"))

    def behaviour(self, input_list: list):
        input_list[0].append(input_list[1])
        return input_list[0]


class ListReplaceAtIndexNode(Node):

    def __init__(self, x, y):
        super().__init__("Replace", Node.COLLECTION_NODE, x, y)
        self.inputs.append((Node.EXEC_TYPE, "Exec"))
        self.inputs.append((Node.LIST_TYPE, "Input List"))
        self.inputs.append((Node.WILDCARD_TYPE, "Item"))
        self.inputs.append((Node.INTEGER_TYPE, "Index"))
        self.outputs.append((Node.EXEC_TYPE, "Exec"))
        self.outputs.append((Node.LIST_TYPE, "Result"))

    def behaviour(self, input_list: list):
        input_list[0][input_list[2]] = input_list[1]
        return input_list[0]


class ListClearNode(Node):

    def __init__(self, x, y):
        super().__init__("Clear", Node.COLLECTION_NODE, x, y)
        self.inputs.append((Node.EXEC_TYPE, "Exec"))
        self.inputs.append((Node.LIST_TYPE, "Input List"))
        self.outputs.append((Node.EXEC_TYPE, "Exec"))
        self.outputs.append((Node.LIST_TYPE, "Result"))

    def behaviour(self, input_list: list):
        return []


class EmptyListNode(Node):

    def __init__(self, x, y):
        super().__init__("Empty List", Node.VARIABLE_NODE, x, y)
        self.outputs.append((Node.LIST_TYPE, "Empty List"))

    def behaviour(self, input_list: list):
        return []