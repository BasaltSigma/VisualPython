from basic_nodes import *
from math_nodes import *

constant_variable_nodes_category = ("Variables", [ConstantBoolNode, ConstantStringNode, ConstantIntNode, ConstantFloatNode,
                                                  EmptyListNode])
boolean_nodes_category = ("Boolean", [BooleanAndNode, BooleanOrNode, BooleanNotNode, BooleanXorNode])
float_nodes_category = ("Float", [FloatAddNode, FloatSubtractNode, FloatMultiplyNode, FloatDivideNode])
string_nodes_category = ("String", [StringConcatenateNode])
basic_functions_nodes_category = ("Utilities", [PrintNode, OpenTextFileNode])
list_nodes_category = ("List", [ListGetAtIndexNode, ListAppendNode, ListClearNode, ListReplaceAtIndexNode])
control_flow_nodes = ("Control Flow", [IfElseNode, ForEachLoopListNode, WhileLoopNode])

all_nodes = [constant_variable_nodes_category, boolean_nodes_category, float_nodes_category, basic_functions_nodes_category,
             string_nodes_category, list_nodes_category, control_flow_nodes]


def factory(class_name):
    inst = globals()[class_name]
    return inst