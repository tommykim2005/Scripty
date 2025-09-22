import tkinter as tk
import customtkinter
from utils.finder import locate_on_screen

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

# root window
root = customtkinter.CTk()
root.geometry("500x500")
root.title("WizBot GUI")

def run_locate():
    # Call your function with an image path
    box = locate_on_screen("images/coin.png")
    if box:
        print("Found at:", box)
    else:
        print("Not found")

# Button
button = customtkinter.CTkButton(master=root, text="Find Image", command=run_locate)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

root.mainloop()