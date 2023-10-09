"""
This script covers the tkinter

Written by Jamal Bouajjaj, 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""
# Tkinter is the GUI framework shown
import tkinter as tk
import colorsys     # for other use
import random

# https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
def _from_rgb(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'


def started1():
    # we make the root top-level
    root = tk.Tk()
    # We run. This will hang until we close
    root.mainloop()

def started2():
    # we make the root top-level
    root = tk.Tk()
    # we add a label
    label1 = tk.Label(root, text="Welcome to tkinter!")
    label1.pack()
    # run
    root.mainloop()

def grid_example():
    # we make the root top-level
    root = tk.Tk()

    title = tk.Label(root, text="TITLE")

    info = tk.Label(root, text="Some Info")
    press1 = tk.Button(root, text="Press Me!")

    title.grid(row=0,column=0,columnspan=2)
    info.grid(row=1,column=0)
    press1.grid(row=1,column=1)

    # run
    root.mainloop()

def button_config_callback():
    def change_button():
        """Function that gets called when the button is pressed"""
        # Get a random color
        c = colorsys.hsv_to_rgb(random.random(), 1, 0.8)
        c = [int(i*255) for i in c]
        c = _from_rgb(*c)
        # Change the button's config, which can include anything (including color)
        # below will not seem to change color, as mouse is over it
        #button.config(background=c)
        button.config(background=c, activebackground=c)
    # we make the root top-level
    root = tk.Tk()

    button = tk.Button(root, text="Press Me!", command=change_button)
    button.pack()

    # run
    root.mainloop()

def binding():
    def event_info(e):
        print(e)
        print(vars(e))
    # we make the root top-level
    root = tk.Tk()

    default_text = "Nothing underneath here!"
    hidden_text = "Boo!"

    text = tk.Label(root, text=default_text, font='Verdana 20 bold', width=len(default_text))
    text.pack()

    text.bind("<Enter>", lambda x: text.config(text=hidden_text, fg='red'))
    text.bind("<Leave>", lambda x: text.config(text=default_text, fg='black'))

    root.bind("a", event_info)
    root.bind("q", lambda x: root.destroy())

    # run
    root.mainloop()

if __name__ == "__main__":
    # Uncomment any below to run

    #started1()
    #started2()
    #grid_example()
    #button_config_callback()
    binding()
