import tkinter as tk
import tkinter.ttk as ttk
import node_map
import basic_nodes
import vp_executor
import node_registry as nr

node_colours = {node_map.Node.DEFAULT_FUNCTION_NODE: "#bc56b4",
                node_map.Node.CONTROL_FLOW_NODE: "#ababab",
                node_map.Node.FUNCTION_NODE: "#2885ff",
                node_map.Node.VARIABLE_NODE: "#fff83a",
                node_map.Node.COLLECTION_NODE: "#ffb247",
                node_map.Node.MATHEMATICAL_NODE: "#0fe200"}
type_colours = {node_map.Node.EXEC_TYPE: "#ffffff",
                node_map.Node.WILDCARD_TYPE: "#000000",
                node_map.Node.BOOL_TYPE: "#c1002d",
                node_map.Node.DICT_TYPE: "#ff7214",
                node_map.Node.FLOAT_TYPE: "#00e408",
                node_map.Node.INTEGER_TYPE: "#efe415",
                node_map.Node.LIST_TYPE: "#45efea",
                node_map.Node.OBJECT_TYPE: "#0e9bef",
                node_map.Node.TUPLE_TYPE: "#0e08ef",
                node_map.Node.SET_TYPE: "#9040ed",
                node_map.Node.STRING_TYPE: "#ed4ed5"}


def create_gui(mi_instance):
    window = tk.Tk()
    window.title("Visual Python: untitled.vpy")
    window.geometry("1280x860")
    toolbar = tk.Frame()
    toolbar.pack(fill=tk.X)
    run_button = tk.Button(toolbar, text="Run")
    run_button.pack(side=tk.LEFT)
    run_button.bind("<Button-1>", executor.execute_start)
    save_button = tk.Button(toolbar, text="Save")
    save_button.pack(side=tk.LEFT)
    save_button.bind("<Button-1>", mi_instance.on_save_button_clicked)
    canvas = tk.Canvas()
    canvas.pack(fill=tk.BOTH, expand=1)
    canvas.bind("<Button-1>", mi_instance.on_mouse_1_down_for_canvas)
    canvas.bind("<B1-Motion>", mi_instance.on_mouse_1_dragged_for_canvas)
    canvas.bind("<ButtonRelease-1>", mi_instance.on_mouse_1_released_for_canvas)
    canvas.bind("<Button-3>", mi_instance.on_mouse_2_clicked_for_canvas)
    return window, canvas


# constants for drawing nodes etc
TITLE_COLOURED_WINDOW_HEIGHT = 23
INITIAL_VERTICAL_OFFSET = TITLE_COLOURED_WINDOW_HEIGHT + 13
VERTICAL_PARAMETER_SPACING = 18


def compute_width(node: node_map.Node) -> int:
    output_titles = []
    input_titles = []
    for output in node.outputs:
        output_titles.append(len(output[1]))
    for inputw in node.inputs:
        input_titles.append(len(inputw[1]))
    length = 0
    if len(output_titles) != 0:
        length = length + max(output_titles)
    if len(input_titles) != 0:
        length = length + max(input_titles)
    if len(node.display_name) > length:
        length = len(node.display_name)
    return length * 9


def compute_height(node: node_map.Node) -> int:
    return TITLE_COLOURED_WINDOW_HEIGHT + (max(len(node.inputs), len(node.outputs), 1) * 30)


def redraw(canvas: tk.Canvas, current_node_map: node_map.NodeMap, offset_x: int, offset_y: int):
    canvas.delete("all")
    for widget in canvas.winfo_children():
        widget.destroy()
    for node in current_node_map.nodes:
        height = compute_height(node) # TITLE_COLOURED_WINDOW_HEIGHT + (max(len(node.inputs), len(node.outputs), 1) * 30)
        width = compute_width(node) + 10
        hh: int = int(height / 2)
        hw: int = int(width / 2)
        x = node.x - offset_x
        y = node.y - offset_y
        canvas.create_rectangle(x - hw, y - hh, x + hw, y + hh, outline="#000", fill="#bbb", width=2)
        canvas.create_rectangle(x - hw, y - hh, x + hw, (y - hh) + TITLE_COLOURED_WINDOW_HEIGHT,
                                outline="#000", fill=node_colours[node.node_type], width=2, tag="node:" + str(node.id))
        canvas.create_text((x - hw) + 5, (y - hh) + (TITLE_COLOURED_WINDOW_HEIGHT / 2), anchor=tk.W, font="Arial", text=node.display_name)
        vertical_offset = INITIAL_VERTICAL_OFFSET
        current_line = 1
        for input_type in node.inputs:
            canvas.create_oval((x - hw) + 3, (y - hh) + vertical_offset - 5, (x - hw) + 13,
                               (y - hh) + vertical_offset + 5, outline="#000", fill=type_colours[input_type[0]],
                               width=1, tag="node:" + str(node.id) + "|input:" + str(current_line))
            canvas.create_text((x - hw) + 16, (y - hh) + vertical_offset, anchor=tk.W, font="Arial", text=input_type[1])
            vertical_offset = vertical_offset + VERTICAL_PARAMETER_SPACING
            current_line = current_line + 1
        vertical_offset = INITIAL_VERTICAL_OFFSET
        current_line = 1
        for output_type in node.outputs:
            canvas.create_oval((x + hw) - 13, (y - hh) + vertical_offset - 5, (x + hw) - 3,
                               (y - hh) + vertical_offset + 5, outline="#000", fill=type_colours[output_type[0]],
                               width=1, tag="node:" + str(node.id) + "|output:" + str(current_line))
            canvas.create_text((x + hw) - 17, (y - hh) + vertical_offset, anchor=tk.E, font="Arial", text=output_type[1])
            vertical_offset = vertical_offset + VERTICAL_PARAMETER_SPACING
            current_line = current_line + 1
        if isinstance(node, (basic_nodes.ConstantFloatNode, basic_nodes.ConstantIntNode, basic_nodes.ConstantStringNode)):
            field = tk.Entry(canvas, width=11)
            field.bind("<Return>", lambda event: set_node_val(node, field.get()))
            field.pack()
            field.place(x=((x - hw) + 3), y=((y - hh) + TITLE_COLOURED_WINDOW_HEIGHT + 5))
            field.insert(0, str(node.val))
        if type(node) is basic_nodes.ConstantBoolNode:
            bool_val = tk.IntVar()
            chkbox = tk.Checkbutton(canvas, variable=bool_val)
            chkbox.pack()
            chkbox.place(x=((x - hw) + 3), y=((y - hh) + TITLE_COLOURED_WINDOW_HEIGHT + 3))
    for connector in current_node_map.connectors:
        first_x = (connector.from_node.x + (compute_width(connector.from_node) / 2)) - 7
        first_y = (connector.from_node.y - (compute_height(connector.from_node) / 2)) + INITIAL_VERTICAL_OFFSET + \
                  ((connector.output_index - 1) * VERTICAL_PARAMETER_SPACING)
        last_x = (connector.to_node.x - (compute_width(connector.to_node) / 2)) + 8
        last_y = (connector.to_node.y - (compute_height(connector.to_node) / 2)) + INITIAL_VERTICAL_OFFSET + \
                 ((connector.input_index - 1) * VERTICAL_PARAMETER_SPACING)
        first_x = first_x - offset_x
        first_y = first_y - offset_y
        last_x = last_x - offset_x
        last_y = last_y - offset_y
        canvas.create_line(first_x, first_y, first_x - ((first_x - last_x) / 4), first_y, first_x - ((first_x - last_x) / 2),
                           first_y - ((first_y - last_y) / 2), first_x - (((first_x - last_x) / 4) * 3), last_y, last_x,
                           last_y, width=2, smooth=True, fill=type_colours[connector.data_type])


def set_node_val(node: basic_nodes.ConstantNode, val):
    try:
        if node.val_type == node_map.Node.FLOAT_TYPE:
            node.val = float(val)
        elif node.val_type == node_map.Node.INTEGER_TYPE:
            node.val = int(val)
        else:
            node.val = val
    except ValueError:
        print("Invalid entry")


def process_tag(tag) -> (int, str, int):
    trimmed = str.split(tag, ' ')[0]
    parts = str.split(trimmed, '|')
    id_from_tag = int(str.split(parts[0], ':')[1])
    rest = str.split(parts[1], ':')
    mode = rest[0]
    line = int(rest[1])
    return id_from_tag, mode, line


def find_connector_type(id_of_node: int, n_type: str, line: int) -> str:
    node: node_map.Node = current_map.find_node_by_id(id_of_node)
    if n_type == "output":
        return node.outputs[line - 1][0]
    else:
        return node.inputs[line - 1][0]


class MouseInteraction:

    current_node_id = None
    current_mode = None
    current_line = None

    def __init__(self):
        self.last_x: int = 0
        self.last_y: int = 0
        self.current_x: int = 0
        self.current_y: int = 0
        self.movement = True
        self.drawing_connector = False
        self.moving_node = False
        self.treeview = None

    def on_mouse_1_down_for_canvas(self, event):
        if self.treeview is not None:
            self.treeview.destroy()
            self.treeview = None
        l = [work_area.itemcget(obj, 'tags') for obj in work_area.find_overlapping(event.x, event.y, event.x, event.y)]
        if len(l) > 1:
            if l[1].__contains__('|'):
                node_id, mode, line = process_tag(l[1])
                self.movement = False
                self.drawing_connector = True
                MouseInteraction.current_mode = mode
                MouseInteraction.current_node_id = node_id
                MouseInteraction.current_line = line
                work_area.create_line(0, 0, 0, 0, tag="current_connector")
            else:
                node_id = int(str.split(str.split(l[1], ' ')[0], ':')[1])
                self.movement = False
                self.moving_node = True
                MouseInteraction.current_node_id = node_id
        else:
            self.movement = True
            self.moving_node = False
            self.drawing_connector = False
        self.last_x = event.x
        self.last_y = event.y

    def on_mouse_1_dragged_for_canvas(self, event):
        self.current_x = self.last_x - event.x
        self.current_y = self.last_y - event.y
        if self.movement and not self.drawing_connector and not self.moving_node:
            redraw(work_area, current_map, self.current_x, self.current_y)
        if self.drawing_connector and not self.moving_node and not self.movement:
            work_area.delete("current_connector")
            work_area.create_line(self.last_x, self.last_y, self.last_x - ((self.last_x - event.x) / 4), self.last_y,
                                  self.last_x - ((self.last_x - event.x) / 2), self.last_y - ((self.last_y - event.y) / 2),
                                  self.last_x - (((self.last_x - event.x) / 4) * 3), event.y,
                                  event.x, event.y, smooth=True, width=2, tag="current_connector",
                                  fill=type_colours[find_connector_type(MouseInteraction.current_node_id,
                                                                        MouseInteraction.current_mode, MouseInteraction.current_line)])
        if self.moving_node and not self.drawing_connector and not self.movement:
            n: node_map.Node = current_map.find_node_by_id(MouseInteraction.current_node_id)
            n.x = event.x
            n.y = event.y
            redraw(work_area, current_map, 0, 0)

    def on_mouse_1_released_for_canvas(self, event):
        if not self.movement and not self.moving_node and self.drawing_connector:
            work_area.delete("current_connector")
            self.drawing_connector = False
            self.movement = True
            l = [work_area.itemcget(obj, 'tags') for obj in work_area.find_overlapping(event.x, event.y, event.x, event.y)]
            if len(l) > 1:
                new_node_id, new_mode, new_line = process_tag(l[1])
                if new_mode == "input":
                    current_map.add_connector(node_map.Connector(current_map.find_node_by_id(MouseInteraction.current_node_id),
                                                                 current_map.find_node_by_id(new_node_id), MouseInteraction.current_line,
                                                                 new_line, find_connector_type(MouseInteraction.current_node_id,
                                                                                               MouseInteraction.current_mode,
                                                                                               MouseInteraction.current_line)))
            MouseInteraction.current_node_id = None
            MouseInteraction.current_line = None
            MouseInteraction.current_mode = None
            redraw(work_area, current_map, 0, 0)
        if not self.movement and not self.drawing_connector and self.moving_node:
            self.moving_node = False
            self.movement = True
            MouseInteraction.current_node_id = None

    def on_mouse_2_clicked_for_canvas(self, event):
        if self.treeview is not None:
            self.treeview.destroy()
            self.treeview = None
        self.treeview = ttk.Treeview(work_area)
        self.treeview.column("#0", width=150, minwidth=150, stretch=tk.NO)
        self.treeview.heading("#0", text="Function Name", anchor=tk.W)
        count = 1
        for category in nr.all_nodes:
            current = self.treeview.insert("", index=count, text=category[0], values=())
            for node in category[1]:
                temp = node(0, 0)
                self.treeview.insert(current, index="end", text=temp.display_name, values=node)
                del temp
            count = count + 1
        self.treeview.pack()
        self.treeview.place(x=event.x, y=event.y)
        self.treeview.bind("<Double-1>", self.on_treeview_item_double_clicked)

    def on_treeview_item_double_clicked(self, event):
        item = self.treeview.selection()[0]
        class_path = self.treeview.item(item, "values")[1][1:-2]
        class_name = str.split(class_path, ".")[1]
        current_map.add_node(nr.factory(class_name)(event.x, event.y))
        self.treeview.destroy()
        self.treeview = None
        redraw(work_area, current_map, self.current_x, self.current_y)

    def on_save_button_clicked(self, event):
        current_map.save_nodemap("untitled")


mi = MouseInteraction()
current_map = node_map.NodeMap()
executor = vp_executor.Executor(current_map)
gui, work_area = create_gui(mi)
current_map.add_node(basic_nodes.StartNode(500, 300))
redraw(work_area, current_map, mi.current_x, mi.current_y)
gui.mainloop()