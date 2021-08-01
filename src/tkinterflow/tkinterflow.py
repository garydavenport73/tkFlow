from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, Listbox, \
    Menubutton, Message, Radiobutton, Scale, Scrollbar, Text, Spinbox, \
    LabelFrame, PanedWindow


def organizeWidgetsWithGrid(frame):
    slaves = frame.pack_slaves()
    for slave in slaves:
        slave.flow(mode='grid')
    slaves = frame.place_slaves()
    for slave in slaves:
        slave.flow(mode='grid')

    _reorganizeWidgetsWithGrid(frame)
    frame.bind("<Configure>", lambda event: _reorganizeWidgetsWithGrid(frame))
    _reorganizeWidgetsWithGrid(frame)


def organizeWidgetsWithPlace(frame):
    # _unpack_unplace_ungrid(frame)
    slaves = frame.pack_slaves()
    for slave in slaves:
        slave.flow(mode='place')
    slaves = frame.grid_slaves()
    for slave in slaves:
        slave.flow(mode='place')

    _reorganizeWidgetsWithPlace(frame)
    frame.bind("<Configure>", lambda event: _reorganizeWidgetsWithPlace(frame))
    _reorganizeWidgetsWithPlace(frame)


def stopOrganizingWidgets(frame):
    frame.unbind("<Configure>")


def _reorganizeWidgetsWithGrid(frame):
    widgetsFrame = frame
    widgetDictionary = widgetsFrame.children
    widgetKeys = []  # keys in key value pairs of the childwidgets

    for key in widgetDictionary:
        widgetKeys.append(key)

    # using calls to recursive definition
    for i in range(len(widgetDictionary)):
        row, column = _getGridPosition(
            i, widgetsFrame, widgetDictionary, widgetKeys)
        widgetDictionary[widgetKeys[i]].grid(row=row, column=column)
        widgetsFrame.update()
        widgetsFrame.update_idletasks()

# given widget i, return its column, row, based on widgets before i, all
# widgets before widget i must have already been gridded


def _getGridPosition(i, widgetsFrame, widgetDictionary, widgetKeys):

    widgetsFrame.update()
    widgetsFrame.update_idletasks()

    for key in widgetDictionary:
        widgetKeys.append(key)

    if i == 0:
        row = 0
        column = 0
        return row, column

    lastWidgetsRow = widgetDictionary[widgetKeys[i-1]].grid_info()["row"]
    lastWidgetsColumn = widgetDictionary[widgetKeys[i-1]].grid_info()["column"]

    # returns the right sided x value of the previous widget
    width = widgetsFrame.grid_bbox(
        row=0, column=0, row2=lastWidgetsRow, col2=lastWidgetsColumn)[2]

    if width+widgetDictionary[widgetKeys[i]].winfo_width() > widgetsFrame.winfo_width():
        # return the last widget row+1, 0
        row = widgetDictionary[widgetKeys[i-1]].grid_info()["row"] + 1
        column = 0
    else:
        # return the last widget row, col+1
        row = widgetDictionary[widgetKeys[i-1]].grid_info()["row"]
        column = widgetDictionary[widgetKeys[i-1]].grid_info()["column"] + 1

    return row, column


def _reorganizeWidgetsWithPlace(frame):
    widgetsFrame = frame
    widgetDictionary = widgetsFrame.children
    widgetKeys = []  # keys in key value pairs of the childwidgets

    for key in widgetDictionary:
        widgetKeys.append(key)

    width = 0
    i = 0
    x = 0
    y = 0
    height = 0
    maxheight = 0
    while i < len(widgetDictionary):
        height = widgetDictionary[widgetKeys[i]].winfo_height()
        if height > maxheight:
            maxheight = height

        width = width + widgetDictionary[widgetKeys[i]].winfo_width()

        # always place first widget at 0,0
        if i == 0:
            x = 0
            y = 0
            width = widgetDictionary[widgetKeys[i]].winfo_width()

        # if after adding width, this exceeds the frame width, bump
        # widget down.  Use maximimum height so far to bump down
        # set x at 0 and start over with new row
        elif width > widgetsFrame.winfo_width():
            y = y + maxheight
            x = 0
            width = widgetDictionary[widgetKeys[i]].winfo_width()
            maxheight = height

        # if after adding width, the widget row length does not exceed
        # frame with, add the widget at the start of last widget's
        # x value

        else:
            x = width-widgetDictionary[widgetKeys[i]].winfo_width()

        # place the widget at the determined x value
        widgetDictionary[widgetKeys[i]].place(x=x, y=y)
        i += 1
    widgetsFrame.update()


def _errorMessage():
    print("cannot be used at root level.  Put frame in root level and use frame")


def _flow(self, mode, cnf={}, **kw):
    # print(mode)
    if (str(self.master) == "."):
        _errorMessage()
        return

    if mode == "grid":
        self.master.bind(
            "<Configure>", lambda event: _reorganizeWidgetsWithGrid(self.master))
        self.master.update()
        _reorganizeWidgetsWithGrid(self.master)

    if mode == "place":
        self.master.bind(
            "<Configure>", lambda event: _reorganizeWidgetsWithPlace(self.master))
        self.master.update()
        _reorganizeWidgetsWithPlace(self.master)


def _flow_destroy(widget, mode):
    widget.destroy()
    widget.master.update()
    widget.master.update_idletasks()
    if mode == "grid":
        _reorganizeWidgetsWithGrid(widget.master)
    if mode == "place":
        _reorganizeWidgetsWithPlace(widget.master)


class FlowButton(Button):
    def __init__(self, *args, **kwargs):
        super(FlowButton, self).__init__(*args, **kwargs)
        self.mode = "grid"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super(FlowCanvas, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowCheckbutton(Checkbutton):
    def __init__(self, *args, **kwargs):
        super(FlowCheckbutton, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowEntry(Entry):
    def __init__(self, *args, **kwargs):
        super(FlowEntry, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowFrame(Frame):
    def __init__(self, *args, **kwargs):
        super(FlowFrame, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowLabel(Label):
    def __init__(self, *args, **kwargs):
        super(FlowLabel, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowListbox(Listbox):
    def __init__(self, *args, **kwargs):
        super(FlowListbox, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowMenubutton(Menubutton):
    def __init__(self, *args, **kwargs):
        super(FlowMenubutton, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowMessage(Message):
    def __init__(self, *args, **kwargs):
        super(FlowMessage, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowRadiobutton(Radiobutton):
    def __init__(self, *args, **kwargs):
        super(FlowRadiobutton, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowScale(Scale):
    def __init__(self, *args, **kwargs):
        super(FlowScale, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowScrollbar(Scrollbar):
    def __init__(self, *args, **kwargs):
        super(FlowScrollbar, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowText(Text):
    def __init__(self, *args, **kwargs):
        super(FlowText, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowSpinbox(Spinbox):
    def __init__(self, *args, **kwargs):
        super(Spinbox, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowLabelFrame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super(FlowLabelFrame, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


class FlowPanedWindow(PanedWindow):
    def __init__(self, *args, **kwargs):
        super(FlowPanedWindow, self).__init__(*args, **kwargs)
        self.mode = "place"

    def flow(self, mode="grid", *args, **kwargs):
        if mode == "place":
            self.mode = "place"
        else:
            self.mode = "grid"
        _flow(self, self.mode, *args, **kwargs)

    def flow_destroy(self):
        _flow_destroy(self, self.mode)


Button = FlowButton
Canvas = FlowCanvas
Checkbutton = FlowCheckbutton
Entry = FlowEntry
Frame = FlowFrame
Label = FlowLabel
Listbox = FlowListbox
Menubutton = FlowMenubutton
Message = FlowMessage
Radiobutton = FlowRadiobutton
Scale = FlowScale
Scrollbar = FlowScrollbar
Text = FlowText
Spinbox = FlowSpinbox
LabelFrame = FlowLabelFrame
PanedWindow = FlowPanedWindow
