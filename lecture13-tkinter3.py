"""
This script covers the tkinter

Written by Jamal Bouajjaj, 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""
# Tkinter is the GUI framework shown
import tkinter as tk
import tkinter.messagebox as messagebox
from enum import Enum

class TkinterColor:
    default_bg = '#ffabba'
    button = '#11ebff'
    button_active = '#1160ff'


class TkinterStyle:
    title = {'font': 'Verdanan 32 bold'}
    label = {'font': 'Verdanan 20'}
    button = {'font': 'Verdanan 20',
              'bg': TkinterColor.button,
              'activebackground': TkinterColor.button_active}
    entry = {'font': 'Verdanan 20', 'bg': 'white', 'relief': 'flat'}
    frame = {'padx': 5, 'pady': 5}
    root = {'background': '#ff9e2f'}


class LabelEntry(tk.Frame):
    def __init__(self, parent, text: str, row: int):
        super().__init__(parent, **TkinterStyle.frame)

        text += ":" # add a :

        self.label = tk.Label(parent, text=text, **TkinterStyle.label)
        self.entry = tk.Entry(parent, **TkinterStyle.entry)

        #self.label.pack(side=tk.LEFT)
        #self.entry.pack()
        self.label.grid(row=row,column=0,sticky='w', pady=2, padx=7)
        self.entry.grid(row=row,column=1)

    def get(self) -> str:
        return self.entry.get()


class InfoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, **TkinterStyle.frame)

        self.name = LabelEntry(self, "Name", 0)
        self.addr = LabelEntry(self, "Address", 1)
        self.phone = LabelEntry(self, "Phone Number", 2)

        #self.name.pack()
        #self.addr.pack()
        #self.phone.pack()

    def get(self) -> dict:
        return {'name': self.name.get(),
                'addr': self.addr.get(),
                'phone': self.phone.get()
                }

class Root:
    def __init__(self):
        self.r = tk.Tk()
        self.r.config(**TkinterStyle.root)
        self.r.tk_setPalette(background=TkinterColor.default_bg)

        self.title = tk.Label(self.r, text="Info Extractor", **TkinterStyle.title)
        self.info = InfoFrame(self.r)
        self.enter = tk.Button(self.r, text="Submit", command=self.submit, **TkinterStyle.button)

        self.title.pack(pady=5, padx=5)
        self.info.pack(pady=5, padx=5)
        self.enter.pack(pady=5, padx=5)

    def run(self):
        self.r.mainloop()

    def submit(self):
        r = self.info.get()
        print(r)
        messagebox.showinfo("Thanks!", f"Thank you '{r['name']}' for your kromer!")


if __name__ == "__main__":
    # Uncomment any below to run

    r = Root()
    r.run()
