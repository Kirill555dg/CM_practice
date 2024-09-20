from logging import disable
from tkinter import Tk, Entry, Button, Text, Frame
import tkinter as tk

class GUI:
    def __init__(self, terminal):
        self.terminal = terminal

        self.window = Tk()
        self.window.geometry('800x600')
        self.window.resizable(False, False)
        self.window.title("Shell Emulator")

        self.console = Text(borderwidth=1, relief='solid', font=24)
        self.console.configure(state=tk.DISABLED)

        self.enter = Entry(font=24)

        self.butn = Button(text="Enter", font=24)
        self.butn.bind('<Button-1>', self.get_cmd)
        self.enter.bind('<Return>', self.get_cmd)

        self.console.place(x=20, y=10, width=750, height=450)
        self.enter.place(x=20, y=500, height=40, relwidth=0.75)
        self.butn.place(x=700, y=500, height=40)
        self.is_cmd = True

        self.terminal.enableGUI(self)

    def write(self, message):
        self.console.configure(state=tk.NORMAL)
        self.console.insert(tk.END, message)
        self.console.configure(state=tk.DISABLED)
        self.console.see("end")

    def get_cmd(self, button):
        command = self.enter.get()
        if self.is_cmd:
            self.terminal.parse_cmd(command)
        else:
            self.terminal.rev_gui(command)
            self.is_cmd = True
        self.enter.delete(0, tk.END)

    def get_text(self):
        self.is_cmd = False


    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.disable)
        self.window.mainloop()

    def disable(self):
        self.terminal.log_file.write(self.terminal.log_file_path)
        self.window.destroy()
        exit()