"""
This script covers the tkinter

Written by Jamal Bouajjaj, 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""
# Tkinter is the GUI framework shown
import tkinter as tk

# Try below
# class LabelEntry(tk.Frame):
#     def __init__(self, parent, text: str):
#         super().__init__(parent)
#
#         text += ":" # add a :
#
#         self.label = tk.Label(self, text=text)
#         self.entry = tk.Entry(self)
#
#         #self.label.pack(side=tk.LEFT)
#         #self.entry.pack()
#         self.label.grid(row=0,column=0)
#         self.entry.grid(row=0,column=1)
#
#     def get(self) -> str:
#         return self.entry.get()


class LabelEntry(tk.Frame):
    def __init__(self, parent, text: str, row: int):
        super().__init__(parent)

        text += ":" # add a :

        self.label = tk.Label(parent, text=text)
        self.entry = tk.Entry(parent)

        #self.label.pack(side=tk.LEFT)
        #self.entry.pack()

        #self.label.grid(row=row,column=0,sticky='w')
        #self.entry.grid(row=row,column=1)

        self.label.grid(row=row,column=0,sticky='w', padx=3, pady=3)
        self.entry.grid(row=row,column=1, pady=3)

    def get(self) -> str:
        return self.entry.get()


class InfoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

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

        self.info = InfoFrame(self.r)
        self.enter = tk.Button(self.r, text="Submit", command=self.submit)

        self.info.pack()
        self.enter.pack()

    def run(self):
        self.r.mainloop()

    def submit(self):
        r = self.info.get()
        print(r)


if __name__ == "__main__":
    # Uncomment any below to run

    r = Root()
    r.run()
