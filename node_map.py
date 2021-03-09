class Node:
    curr_id: int = 0

    CONTROL_FLOW_NODE = 0
    FUNCTION_NODE = 1
    MATHEMATICAL_NODE = 2
    DEFAULT_FUNCTION_NODE = 3
    VARIABLE_NODE = 4
    COLLECTION_NODE = 5

    BOOL_TYPE = "boolean"
    INTEGER_TYPE = "int"
    STRING_TYPE = "str"
    FLOAT_TYPE = "float"
    LIST_TYPE = "list"
    DICT_TYPE = "dict"
    TUPLE_TYPE = "tuple"
    SET_TYPE = "set"
    OBJECT_TYPE = "object"
    EXEC_TYPE = "exec"
    WILDCARD_TYPE = "wildcard"

    def __init__(self, display_name: str, node_type: int, x: int, y: int):
        self.x = x
        self.y = y
        self.display_name = display_name
        self.id = Node.curr_id
        self.inputs = []    # list of tuples of format (type, name)
        self.outputs = []   # ditto
        self.node_type = node_type

    def __eq__(self, other_node):
        return self.id == other_node.id

    def behaviour(self, input_list: list):
        raise NotImplemented()


class ConstantNode(Node):

    def __init__(self, display_name, x, y, value, val_type):
        super().__init__(display_name, Node.VARIABLE_NODE, x, y)
        self.val_type = val_type
        self.val = value
        self.outputs.append((val_type, "Value"))

    def behaviour(self, input_list: list):
        return self.val


class Connector:

    def __init__(self, from_node: Node, to_node: Node, output_index: int, input_index: int, d_type: str):
        if from_node is None or to_node is None:
            raise ReferenceError("Connected nodes cannot be none")
        self.from_node: Node = from_node
        self.to_node: Node = to_node
        self.output_index = output_index
        self.input_index = input_index
        self.data_type = d_type


class NodeMap:

    def __init__(self):
        self.nodes = []
        self.connectors = []

    def add_node(self, node: Node):
        Node.curr_id = Node.curr_id + 1
        self.nodes.append(node)
        node.id = Node.curr_id

    def add_connector(self, connector: Connector):
        self.connectors.append(connector)

    def find_node_by_id(self, specified_id: int) -> Node:
        for node in self.nodes:
            if node.id == specified_id:
                return node
        raise ValueError("node with id " + str(specified_id) + " not found")

    def find_attached_connector(self, node: Node, output=True, line=1) -> Connector:
        if output:
            for connector in self.connectors:
                if connector.from_node == node and connector.output_index == line:
                    return connector
        else:
            for connector in self.connectors:
                if connector.to_node == node and connector.input_index == line:
                    return connector
        return None

    def save_nodemap(self, filename):
        with open("./" + filename + ".vpy", "w+") as my_file:
            my_file.write(filename + '\n')
            print(str(len(self.nodes)) + "," + str(len(self.connectors)))
            for node in self.nodes:
                node_name = str.split(str(node), ' ')[0][1:]
                built_node = "node{" + str(node.id) + "," + node_name + ',x=' + str(node.x) + ",y=" + str(node.y)
                if isinstance(node, ConstantNode):
                    built_node += ",var=" + str(node.val) + ",val_type=" + node.val_type
                built_node += '}\n'
                my_file.write(built_node)
            for connector in self.connectors:
                built_connector = "connector{" + str(connector.from_node.id) + ',' + str(connector.to_node.id) + ','
                built_connector += str(connector.output_index) + ',' + str(connector.input_index) + ',' + connector.data_type + '}\n'
                my_file.write(built_connector)


def begins_with(input_str: str, sequence: str) -> bool:
    return input_str[0:len(sequence)] == sequence


def load_node_map(path):
    from node_registry import factory
    new_node_map = NodeMap()
    with open(path, "r") as my_file:
        lines: list = my_file.read().splitlines()
        for line in lines:
            if begins_with(line, "node"):
                trimmed_node = line[5:-1]
                nparams = str.split(trimmed_node, ',')
                class_name = str.split(nparams[1], '.')[1]
                instance = factory(class_name)
                node = instance(int(str.split(nparams[2], '=')[1]), int(str.split(nparams[3], '=')[1][:-1]))
                node.id = int(nparams[0])
                if isinstance(node, ConstantNode):
                    node.val_type = str.split(nparams[5], '=')[1][:-1]
                    value_to_assign = str.split(nparams[4], '=')[1]
                    if class_name == "ConstantBoolNode":
                        node.val = bool(value_to_assign)
                    elif class_name == "ConstantFloatNode":
                        node.val = float(value_to_assign)
                    elif class_name == "ConstantIntNode":
                        node.val = int(value_to_assign)
                    else:
                        node.val = value_to_assign
                new_node_map.add_node(node)
            elif begins_with(line, "connector"):
                trimmed_connector = line[10:-1]
                params = str.split(trimmed_connector, ',')
                new_node_map.add_connector(Connector(new_node_map.find_node_by_id(int(params[0])),
                                                     new_node_map.find_node_by_id(int(params[1])), int(params[2]),
                                                     int(params[3]), params[4]))
            else:
                continue
    Node.curr_id = len(new_node_map.nodes) + 1
    return new_node_map
