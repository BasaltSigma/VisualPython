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
        Node.curr_id = Node.curr_id + 1
        self.inputs = []    # list of tuples of format (type, name)
        self.outputs = []   # ditto
        self.node_type = node_type

    def __eq__(self, other_node):
        return self.id == other_node.id

    def behaviour(self, input_list: list):
        raise NotImplemented()


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
        self.nodes.append(node)

    def add_connector(self, connector: Connector):
        self.connectors.append(connector)

    def find_node_by_id(self, specified_id: int) -> Node:
        for node in self.nodes:
            if node.id == specified_id:
                return node
        raise ValueError("node with id " + str(specified_id) + " not found")

    def save_nodemap(self, filename):
        with open("./" + filename + ".vpy", "w+") as my_file:
            my_file.write(filename)
            for node in self.nodes:
                pass