from tkinter import *
from PIL import Image, ImageTk
import os
import telepot

win=Tk()
win.title("Secret Message")
win.configure(background="#fff0ff")
win.geometry("1540x800")


img=Image.open("msgg.jpg")
img=img.resize((1500, 750))
bg=ImageTk.PhotoImage(img)

lbl=Label(win,image=bg)
lbl.place(x=15,y=15)


lbl=Label(win,text="Authenticated Successfull",font=("times",30,"bold"),bg="#ffc34d",fg="black")
lbl.place(x=500,y=15)

lbl=Label(win,text="Enter the Message Here....",font=("times",30,"bold"),bg="#ffc34d",fg="black")
lbl.place(x=100,y=150)

entry=Entry(win,text="",font=("times",24,"bold"),bg="#ffc34d",fg="black",justify=CENTER)
entry.place(x=175,y=225)

entry.insert(0,"   ")
###########################################################################################################################
def data():
    global message
    message=entry.get()
    def show():
        name=clicked.get()
        label.config( text ="You choosed: \n  "+str(name),bg="#ffc34d")
        if name=="Brigadier":
            print("message sent to {} is {}".format(name,message))
        elif name=="Colonel":
            print("message sent to {} is {}".format(name,message))
        elif name=="Lieutinant_colonel":
            print("message sent to {} is {}".format(name,message))
        elif name=="Major":
            print("message sent to {} is {}".format(name,message))
        lab_ack=Label(win,text="Messaged Sent Sucessfull to \n  "+str(name),font=("times",24,"bold"),bg="#ffc34d",fg="black")
        lab_ack.place(x=1100,y=250)
    # Dropdown menu options
    options = [
        "Brigadier",
        "Colonel",
        "Lieutinant_colonel",
        "Major",
        
    ]
      
    # datatype of menu text
    clicked = StringVar()
      
    # initial menu text
    clicked.set( "person1" )
      
    # Create Dropdown menu
    drop = OptionMenu( win , clicked , *options )
    drop.place(x=600,y=150)
    drop.configure(font=("times",20,"bold"),bg="#ffc34d")

    # Create button, it will change label text
    button = Button( win , text = "CONFIRM" , command = show ,font=("times",20,"bold"),bg="#ffe6cc",fg="black",activebackground="red")
    button.place(x=950,y=150)
      
    # Create Label
    label = Label( win , text = " " ,font=("times",20,"bold"),fg="black")
    label.place(x=1150,y=150)

################################################################################################################################

btn=Button(win,text="Send msg ",font=("times",24,"bold"),bg="#ffe6cc",fg="black",command=data,activebackground="red")
btn.place(x=250,y=300)

win.mainloop()






