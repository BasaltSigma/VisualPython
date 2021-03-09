import node_map as nm
from basic_nodes import *

class Executor:

    def __init__(self, curr_node_map: nm.NodeMap):
        self.curr_node_map = curr_node_map

    def execute_start(self, event):
        start: nm.Node = self.curr_node_map.find_node_by_id(1)
        start.behaviour([])
        running = True
        current_node = start
        while running:
            out_connector = self.curr_node_map.find_attached_connector(current_node, output=True, line=1)
            if out_connector is None:
                running = False
                break
            current_node = out_connector.to_node
            input_vals = []
            if len(current_node.inputs) > 1:
                for i in range(2, len(current_node.inputs) + 1):
                    input_vals.append(self.execute_pure(current_node, i, True))

    def execute_pure(self, node: nm.Node, line: int, base: bool):
        if isinstance(node, (ConstantIntNode, ConstantFloatNode, ConstantStringNode, ConstantBoolNode)) and not base:
            return node.behaviour([])
        input_list = []
        for i in range(2, len(node.inputs) + 1):
            connector = self.curr_node_map.find_attached_connector(node, output=False, line=i)
            input_list.append(self.execute_pure(connector.from_node, i, False))
        return node.behaviour(input_list)