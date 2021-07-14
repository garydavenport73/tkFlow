# tkinterflow

This is a project to add the functionality of a 'flow layout' to Python Tkinter graphical user interface module. Right now, Tkinter has the Pack, Grid, and Place geometry managers. I would like it to have Flow, and the behavior or a widget using the Flow geometry manager would be like text wrapping. 

To implement the module, of course install it first with:
```
pip install tkinterflow
```
then use the following import statements
```
from tkinter import *
from tkinter.flow import *
```
Now instead of using statments like:
```
button.pack()
```
you can use
```
button.flow()
```
for flow behaviour

the flow behavior is a subset of the grid geometry manager.

