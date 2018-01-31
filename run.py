import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import sys
import os
import platform
import subprocess
import threading
import csv
from pprint import pprint
import lib.bulk as bulk
import json


class App(object):
    root = tk.Tk()
    input_file = tk.StringVar()
    input_data = None
    template_file = tk.StringVar()
    template_data = None
    sites_number = tk.StringVar()


    def __init__(self, title=""):
        os.makedirs("templates", exist_ok=True)
        os.makedirs("results", exist_ok=True)
        if not os.path.exists("lib"):
            raise BaseException("lib folder missing!")
        self.start_time = time.time()
        self.root.title(title)
        self.root.minsize(width=200, height=170)  # height=200)
        self.root.resizable(width=False, height=False)
        self.root.configure(background='#EAEAEA')
        self.input_file.set("input file: ")
        self.template_file.set("template file: ")

        self.call_GUI()

    def call_GUI(self):
        GUI(self)

    def start(self):
        self.root.mainloop()


class GUI(object):

    def __init__(self, app):
        self.root_frame = ttk.Frame(app.root)
        self.startbutton = None
        self.button_width = 6

        for method in GUI.__dict__:
            if method.startswith('add_'):
                print(method)
                GUI.__dict__[method](self)
        self.root_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        print('Loaded...')


    def add_topbar(self):
        topbar = ttk.Frame(self.root_frame, height=50)
        l = ttk.Label(topbar, text="Nivel Webcrawler", font=("Helvetica", 28))
        l.pack(side=tk.LEFT)
        topbar.pack(side=tk.TOP, fill=tk.X)

    def add_functionbar(self):
        functionbar = ttk.Frame(self.root_frame)
        functionbar.pack()
        b1 = ttk.Button(functionbar,
                           text="input",
                           command=Buttons.button1)
        b1.pack(side=tk.LEFT)
        b2 = ttk.Button(functionbar,
                        text="template",
                        command=Buttons.button2)
        b2.pack(side=tk.LEFT)
        b3 = ttk.Button(functionbar,
                        text="output",
                        command=Buttons.button3)
        b3.pack(side=tk.LEFT)


    def add_varspace1(self):
        ttk.Frame(self.root_frame, height=35).pack(fill=tk.BOTH)

    def add_statusbar(self):
        statusbar = ttk.Frame(self.root_frame)
        statusbar.pack()
        l1 = ttk.Label(statusbar, textvariable=App.input_file)
        l1.pack()

        l2 = ttk.Label(statusbar, textvariable=App.template_file)
        l2.pack()

        l2 = ttk.Label(statusbar, textvariable=App.sites_number)
        l2.pack()

    def add_varspace2(self):
        ttk.Frame(self.root_frame, height=20).pack(fill=tk.BOTH)


    def add_startbar(self):
        startbar = ttk.Frame(self.root_frame)
        startbar.pack()
        startbutton = ttk.Button(startbar,
                           text="start",
                           command=Buttons.start_button)
        startbutton.pack()

class Buttons(object):
    @staticmethod
    def button1():
        path = filedialog.askopenfilename(initialdir=".", title="Select input file",
                                          filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        with open(path, 'r') as f:
            file = f.readlines()
        sites = []
        for url in file:
            url = url.strip()
            if '://' not in url:
                url = ''.join(['http://', url])
            sites.append(url)

        App.input_file.set(f"input file: {os.path.basename(path)}")
        App.input_data = sites
        App.sites_number.set(f"sites: {len(sites)}")


    @staticmethod
    def button2():
        path = filedialog.askopenfilename(initialdir=os.path.join('.', 'templates'), title="Select template file",
                                          filetypes=(("json files", "*.json"), ("all files", "*.*")))

        try:
            with open(path, encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
        except ValueError:
            messagebox.showerror("Error", "Invalid template!\nThe selected file is not valid JSON. Use webscraper.io to create a json site map.")
            return

        App.template_file.set(f"template file: {os.path.basename(path)}")
        App.template_data = path

    @staticmethod
    def button3():
        path = "results"
        if platform.system() == "Windows":
            path = path.replace("/", "\\")
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    @staticmethod
    def start_button():
        if not App.input_data:
            messagebox.showerror("Error", "No input file selected!\nSelect .txt file containing URL's")
            return
        elif not App.template_data:
            messagebox.showerror("Error", "No template file selected!\nSelect a valid .json file")
            return

        App.root.withdraw()
        bulk.run(input_data=App.input_data, template=App.template_data)


if __name__ == '__main__':
    app = App(title="")
    print('Starting...')
    app.start()


