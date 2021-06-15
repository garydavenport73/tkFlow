# tkFlow

This is a project to add the functionality of a 'flow layout' to Python Tkinter graphical user interface module. Right now, Tkinter has the Pack, Grid, and Place geometry managers. I would like it to have Flow, and the behavior or a widget using the Flow geometry manager would be like text wrapping. 

So just as a start, I copied the init.py located at https://github.com/python/cpython/blob/3.9/Lib/tkinter/__init__.py, and modified it. 

I renamed it tkinterFlow.py.

I am posting the original source code first, then making changes so those changes will be highlighted. 

I am also including a sample flowDemo.py to show it in use.
