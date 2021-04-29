from tkinterFlow import *

def main():

    root = Tk()

    root.title("Using \"button.flow()\"")

    myFrame=Frame(root)
    myFrame.pack(fill=BOTH, expand=True)

    button1=Button(myFrame, text="---Button1---")
    button1.flow(sticky=NSEW)
    button2=Button(myFrame, text="---Button2---")
    button2.flow(sticky=NSEW)
    button3=Button(myFrame, text="---Button3---")
    button3.flow(sticky=NSEW)
    button4=Button(myFrame, text="---Button4---")
    button4.flow(sticky=NSEW)
    button5=Button(myFrame, text="---Button5---")
    button5.flow(sticky=NSEW)
    button6=Button(myFrame, text="---Button6---")
    button6.flow(sticky=NSEW)
    button7=Button(myFrame, text="---Button7---")
    button7.flow(sticky=NSEW)

    root.mainloop()

main()


