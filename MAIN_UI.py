from tkinter import *
import os
from PIL import Image,ImageTk


win=Tk()
win.title("FACE RECOGNITION USING CNN")
win.configure(bg="#000000")
win.geometry("1500x750")
img=Image.open("aa.jpg")
img=img.resize((1500,750))
bg=ImageTk.PhotoImage(img)

lbl=Label(win,image=bg)
lbl.place(x=0,y=0)

def run_file():
    command = 'python.exe .\\main.py .\\20170512-110547\\20170512-110547.pb .\\20170512-110547\\ids\\'
    os.system(command)
def data():
    import tkinter as tk

    def save_details():
        name = name_entry.get()
        location = location_entry.get()
        phone_number = phone_entry.get()
        age = age_entry.get()
        gender = gender_entry.get()
        with open("user_details.txt", "a") as f:
            f.write(f"{name}, {location}, {phone_number}, {age}, {gender}\n")
        # Clear the form fields
        name_entry.delete(0, tk.END)
        location_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        gender_entry.delete(0, tk.END)

    # Create the main window
    root = tk.Tk()
    root.title("User Details")

    # Create the form fields
    name_label = tk.Label(root, text="Name:")
    name_entry = tk.Entry(root)

    location_label = tk.Label(root, text="Location:")
    location_entry = tk.Entry(root)

    phone_label = tk.Label(root, text="Phone Number:")
    phone_entry = tk.Entry(root)

    age_label = tk.Label(root, text="Age:")
    age_entry = tk.Entry(root)

    gender_label = tk.Label(root, text="Gender:")
    gender_entry = tk.Entry(root)

    # Add the form fields to the window
    name_label.pack()
    name_entry.pack()

    location_label.pack()
    location_entry.pack()

    phone_label.pack()
    phone_entry.pack()

    age_label.pack()
    age_entry.pack()

    gender_label.pack()
    gender_entry.pack()

    # Create the submit button
    submit_button = tk.Button(root, text="Submit", command=save_details)
    submit_button.pack()

    # Start the main loop
    root.mainloop()
def photo():
    import tkinter as tk
    from tkinter import filedialog
    import os

    def select_image():
        # Open a file dialog to select an image file
        image_file = filedialog.askopenfilename(
            initialdir="/", title="Select Image", 
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("all files", "*.*")))
        # Set the text of the image entry widget to the selected file path
        image_entry.delete(0, tk.END)
        image_entry.insert(0, image_file)

    def save_image():
        # Get the selected image file path from the image entry widget
        image_file = image_entry.get()
        # Open a file dialog to select the destination directory
        dest_directory = filedialog.askdirectory(
            initialdir="/", title="Select Destination Folder")
        if dest_directory:
            # Get the destination file path
            dest_file = os.path.join(dest_directory, os.path.basename(image_file))
            # Save the image to the destination file
            with open(dest_file, "wb") as f:
                with open(image_file, "rb") as src_file:
                    f.write(src_file.read())
            # Display a message to the user
            message_label.config(text="Image saved successfully.")
        else:
            # Display an error message to the user
            message_label.config(text="Error: No destination folder selected.")

    # Create the tkinter window
    window = tk.Tk()

    # Create the widgets for the form
    image_label = tk.Label(window, text="Image:")
    image_entry = tk.Entry(window)
    image_button = tk.Button(window, text="Select Image", command=select_image)
    save_button = tk.Button(window, text="Save Image", command=save_image)
    message_label = tk.Label(window, text="")

    # Layout the widgets using the grid geometry manager
    image_label.grid(row=0, column=0)
    image_entry.grid(row=0, column=1)
    image_button.grid(row=0, column=2)
    save_button.grid(row=1, column=1)
    message_label.grid(row=2, column=0, columnspan=3)

    # Start the tkinter event loop
    window.mainloop()

        
label=Label(win,text=" AGE INARIANT FACE RECOGNITION USING CNN",bg="black",fg="white",font=("times",25,"bold"))
label.place(x=200,y=25)

label=Label(win,text=" Click below button to run the project",bg="black",fg="white",font=("times",22,"bold"))
label.place(x=750,y=150)

label=Button(win,text="Start",bg="black",fg="white",font=("times",25,"bold"),command=run_file)
label.place(x=800,y=240)

label=Button(win,text="enter_data",bg="black",fg="white",font=("times",25,"bold"),command=data)
label.place(x=800,y=340)

label=Button(win,text="upload a photo",bg="black",fg="white",font=("times",25,"bold"),command=photo)
label.place(x=800,y=440)


win.mainloop()

