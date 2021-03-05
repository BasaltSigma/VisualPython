import node_map as nm
import basic_nodes

class Executor:

    def __init__(self, curr_node_map: nm.NodeMap):
        self.curr_node_map = curr_node_map

    def execute(self):
        start: nm.Node = None
        for n in self.curr_node_map.nodes:
            if type(n) is basic_nodes.StartNode:
                start = n
        start.behaviour([])