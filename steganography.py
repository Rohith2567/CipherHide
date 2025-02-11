from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
from stegano import lsb

from tkinter import messagebox
from tkinter import ttk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = Tk()
root.title("CipherHide - Hide a Secret Text Message in an Image")
root.geometry("700x500+150+180")
# root.eval("tk::PlaceWindow . center")
root.resizable(False, False)
# #3d6466
# #2f4155
root.configure(bg="#2f4155")

filename = None
secret = None


def messagebox2(typ, title, message):
    toplevel = Toplevel(root)

    toplevel.title(title)
    toplevel.geometry("300x85+350+380")

    img = PhotoImage(file=resource_path("logo.jpg"))
    toplevel.iconphoto(True, img)

    if typ == "Warning":
        l1 = Label(toplevel, image="::tk::icons::warning")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
    elif typ == "Error":
        l1 = Label(toplevel, image="::tk::icons::error")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
    elif typ == "Save":
        l1 = Label(toplevel, image="::tk::icons::information")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
    else:
        l1 = Label(toplevel, image="::tk::icons::question")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")

    l2 = Label(toplevel, text=message)
    l2.grid(row=0, column=1, columnspan=3, pady=(7, 10), sticky="w")

    b1 = Button(toplevel, text="ok", command=toplevel.destroy, width=10)
    b1.grid(row=1, column=1, padx=(2, 35), sticky="e")


def show_image():
    global filename

    text1.delete(1.0, END)
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetypes=(("PNG file", "*.png"),
                                                     ("JPG File", "*.jpg"), ("All File", "*.txt")))

    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img, width=250, height=250)
    lbl.image = img


def hide():
    global secret

    if not filename:
        messagebox2("Error", "Image Error", "No Image")
        # messagebox.showerror("Image Error", "No Image")
    else:
        message = text1.get(1.0, END)
        if message == "\n":
            messagebox2("Error", "Hide Error", "No Input")
            # messagebox.showerror("Hide Error", "No Input")
        else:
            secret = lsb.hide(str(filename), message)
            # messagebox.showinfo("Success", "Valid input!")


def save():
    if not filename:
        messagebox2("Error", "Image Error", "No Image")
        # messagebox.showerror("Image Error", "No Image")
    else:
        fn = os.path.basename(filename)
        name, extension = os.path.splitext(fn)
        f_name = name + "_hidden" + extension
        # print(f_name)
        if not secret:
            messagebox2("Warning", "Save Warning", "No message to save")
            # messagebox.showerror("Save Error", "No message to save")
        else:
            secret.save(f_name)
            messagebox2("Save", "Save Info", "Image saved successfully")


def show():

    if not filename:
        messagebox2("Error", "Image Error", "No Image")
        # messagebox.showerror("Image Error", "No Image")
    else:
        try:
            clear_message = lsb.reveal(filename)

            if clear_message:
                # text1.delete(1.0, END)
                text1.insert(END, clear_message)

        except IndexError:
            # messagebox.showwarning("Warning", "No Hidden Data")
            messagebox2("Warning", "Warning", "No Hidden Data")
        except Exception as e:
            messagebox.showerror("Error", f"An error occured: {str(e)}")


# frame = tk.Frame(root, width=500, height=600, bg="#3d6466")
# frame.grid(row=0, column=0)

# icon
image_icon = PhotoImage(file=resource_path("logo.jpg"))
root.iconphoto(False, image_icon)

# logo
logo = PhotoImage(file=resource_path("logo_lock.png"))
# Label(root, image=logo, bg="#2f4155").pack()
Label(root, image=logo, bg="#2f4155").place(x=10, y=0)

Label(root, text="CYBER SCIENCE", bg="#2f4155", fg="white", font="arial 25 bold").place(x=100, y=20)

# first Frame
f = Frame(root, bd=3, bg="#2A2A2A", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="#2A2A2A")
lbl.place(x=40, y=10)

# second Frame
frame2 = Frame(root, bd=3, width=340, height=280, bg="#F5F5F5", relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font="Robot 20", bg="#F5F5F5", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# third Frame
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

# style = ttk.Style()
# style.configure("Rounded.TButton", width=10, height=2, font=("arial", 12, "bold"), background="#2f4155",
#                 foreground="black", padding=10,
#                 borderwidth=0, relief="groove")
# style.map("Rounded.TButton", background=[("active", "lightblue")])
#
# button = ttk.Button(frame3, text="Open Image", style="Rounded.TButton",command=lambda: print("Clicked!"))
# button.place(x=20, y=30)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=show_image).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Label(frame3, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# third Frame
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=show).place(x=180, y=30)
Label(frame4, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

root.mainloop()
