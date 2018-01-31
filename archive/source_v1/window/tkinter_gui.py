import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import time
import threading


class App:
    def __init__(self, webcrawler, title="Application window"):
        self.WebCrawler = webcrawler
        self.start_time = time.time()
        self.root = tk.Tk()
        self.root.title(title)
        self.root.resizable(width=False, height=False)
        self.toolbar = None
        self.logbox = None
        self.progressbar = None
        self.input_file = tk.StringVar()
        self.progress = 0
        self.urls = []
        self.tasks = []

        for method in App.__dict__:
            if method.startswith('add_'):
                print(method)
                App.__dict__[method](self)
        print('Loaded...')

    def add_toolbar(self):
        self.toolbar = ttk.Frame(self.root)
        b = ttk.Button(self.toolbar, text="crawl", width=6, command=self.start_crawl)
        b.pack(side=tk.LEFT, padx=2, pady=2)
        b = ttk.Button(self.toolbar, text="bron", width=6, command=self.pick_input)
        b.pack(side=tk.LEFT, padx=2, pady=2)
        self.input_file_label = ttk.Label(self.toolbar, textvariable=self.input_file)
        self.input_file_label.pack(side=tk.LEFT, padx=2, pady=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def add_logbox(self):
        self.logbox = tk.Text(self.root, width=80, height=24, wrap='none')
        self.logbox.insert('1.0', 'Welkom bij de NIVEL webcrawler')
        self.logbox.pack(fill=tk.X)
        self.logbox['state'] = 'disabled'

    def _add_progressbar(self):
        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", value=0, maximum=len(self.urls))
        self.progressbar.pack(side=tk.BOTTOM, fill=tk.X)

    def log(self, text):
        numlines = self.logbox.index('end - 1 line').split('.')[0]
        self.logbox['state'] = 'normal'
        if numlines == 24:
            self.logbox.delete(1.0, 2.0)
        if self.logbox.index('end-1c') != '1.0':
            self.logbox.insert('end', '\n')
        self.logbox.insert('end', text)
        self.logbox['state'] = 'disabled'
        self.logbox.yview(tk.END)

    def add_menubar(self):
        menubar = tk.Menu(self.root)
        menu_settings = tk.Menu(menubar)
        menu_settings.add_command(label='Kies bron...', command=self.pick_input)
        menubar.add_cascade(menu=menu_settings, label='Settings')
        self.root.config(menu=menubar)

    def pick_input(self):
        input_file = filedialog.askopenfilename(title="Kies lijst met webadressen", filetypes=[('all_files', '.txt')])

        if input_file:
            self.input_file.set(input_file)
            path = self.input_file.get()
            self.log(f"Gekozen bestand {path}")
            with open(path, 'r') as f:
                for line in f.readlines():
                    if len(line.split()) == 1 and '.' in line:
                        self.urls.append(line)
                    else:
                        self.log(f"Skipped line: \"{line}\"")
                self.log(f"Aantal webadressen: {len(self.urls)}")

    def start_crawl(self):
        input_file = self.input_file.get()
        if not input_file:
            messagebox.showinfo("Rustig aan", "Kies eerst een bron")
            return

        self._add_progressbar()

        crawl_thread = threading.Thread(target=self._crawl)
        self.tasks.append(crawl_thread)
        crawl_thread.start()

        progress_thread = threading.Thread(target=self.progress)
        progress_thread.start()

    def _crawl(self):
        webcrawler = self.WebCrawler.Controller(file=self.input_file.get(), last_line=3,
                                                debug_out=self.log)  # todo add settings lines
        self.log("Begonnen met crawlen...")
        webcrawler.threaded_run()

    def progress(self):
        if self.tasks:
            thread = self.tasks[0]
            print(thread)
            thread.join()
            self.log("Klaar met crawlen...")

    def add_keybinding(self):
        self.root.bind_all('<Return>', None)

    def start(self):
        self.root.mainloop()



if __name__ == '__main__':
    from ..crawler import WebCrawler
    app = App(WebCrawler, title="Nivel")
    print('Starting...')
    app.start()
