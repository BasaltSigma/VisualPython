from basic_nodes import *
from math_nodes import *

constant_variable_nodes_category = ("Variables", [ConstantBoolNode, ConstantStringNode, ConstantIntNode, ConstantFloatNode])
boolean_nodes_category = ("Boolean", [BooleanAndNode, BooleanOrNode, BooleanNotNode, BooleanXorNode])
float_nodes_category = ("Float", [FloatAddNode, FloatSubtractNode, FloatMultiplyNode])
basic_functions_nodes_category = ("Utilities", [PrintNode])

all_nodes = [constant_variable_nodes_category, boolean_nodes_category, float_nodes_category, basic_functions_nodes_category]

""" name_to_class_dict = {"basic_nodes.ConstantBoolNode": ConstantBoolNode, "basic_nodes.ConstantStringNode": ConstantStringNode,
                      "basic_nodes.ConstantFloatNode": ConstantFloatNode, "basic_nodes.ConstantIntNode": ConstantIntNode,
                      "basic_nodes.IfElseNode": IfElseNode, "basic_nodes.PrintNode": PrintNode}"""


def factory(class_name):
    inst = globals()[class_name]
    return inst