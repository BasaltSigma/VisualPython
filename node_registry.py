from basic_nodes import *
from math_nodes import *

constant_variable_nodes_category = ("Variables", [ConstantBoolNode, ConstantStringNode, ConstantIntNode, ConstantFloatNode])
boolean_nodes_category = ("Boolean", [BooleanAndNode, BooleanOrNode, BooleanNotNode, BooleanXorNode])
float_nodes_category = ("Float", [FloatAddNode, FloatSubtractNode, FloatMultiplyNode, FloatDivideNode])
string_nodes_category = ("String", [StringConcatenateNode])
basic_functions_nodes_category = ("Utilities", [PrintNode])

all_nodes = [constant_variable_nodes_category, boolean_nodes_category, float_nodes_category, basic_functions_nodes_category,
             string_nodes_category]


def factory(class_name):
    inst = globals()[class_name]
    return inst