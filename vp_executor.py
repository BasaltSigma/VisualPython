import node_map as nm
import basic_nodes

class Executor:

    def __init__(self, curr_node_map: nm.NodeMap):
        self.curr_node_map = curr_node_map

    def execute(self):
        start: nm.Node = self.curr_node_map.find_node_by_id(0)
        start.behaviour([])
        running = True
        while running:
            pass