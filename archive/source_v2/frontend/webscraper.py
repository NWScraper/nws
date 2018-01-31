import tkinter as tk
from tkinter import ttk
import time
import sys
import os
import platform
import subprocess
import threading
import csv
import backend.scrap as scrap
from pprint import pprint


class App(object):
    running = []
    ran = 0
    def __init__(self, title=""):
        self.webcrawler = scrap.NivelScraper
        self.start_time = time.time()
        self.root = tk.Tk()
        self.root.title(title)
        self.root.minsize(width=400, height=170)#height=200)
        self.root.resizable(width=False, height=False)
        self.root.configure(background='#EAEAEA')
        self.root_frame = ttk.Frame(self.root)
        self.startbutton = None
        self.savebutton = None
        self.progressbar_label_text = None
        self.progressbar_label = None
        self.progressbar = None
        self.site_maps = []
        self.button_width = 10
        self.done_site_maps = 0
        self.tasks = []
        self.saved_files_dir = 'results'
        print(os.path.dirname(sys.argv[0]))
        self.sitemap_root = os.path.join(os.path.dirname(sys.argv[0]), 'sitemaps')
        self.selected_sitemap_dir = tk.StringVar()

        for method in App.__dict__:
            if method.startswith('add_'):
                print(method)
                App.__dict__[method](self)
        self.root_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        self.read_sitemap_dir()
        print('Loaded...')
        if '-r' in sys.argv:
            print('From restart')


    def add_topbar(self):
        topbar = ttk.Frame(self.root_frame, height=50)
        l = ttk.Label(topbar, text="Nivel Webcrawler", font=("Helvetica", 28))
        l.pack(side=tk.LEFT)
        topbar.pack(side=tk.TOP, fill=tk.X)

    def add_startbar(self):
        startbar = ttk.Frame(self.root_frame)
        self.startbutton = ttk.Button(startbar, text="Start", width=self.button_width, command=self.start_crawl)
        self.startbutton.pack(side=tk.LEFT, pady=10)
        b2 = ttk.Button(startbar, text="Sitemaps", width=self.button_width, command=self.open_site_map_dir)
        b2.pack(side=tk.LEFT, pady=10)
        # b3 = ttk.Button(startbar, text="Editor", width=self.button_width, command=self.open_editor)
        # b3.pack(side=tk.LEFT, pady=10)
        startbar.pack(side=tk.TOP, fill=tk.X)


    def add_varspace(self):
        ttk.Frame(self.root_frame, height=35).pack(fill=tk.BOTH)

    def add_savebar(self):
        savebar = ttk.Frame(self.root_frame)
        self.savebutton = ttk.Button(savebar, text="Resultaten", width=self.button_width, command=self.open_saved_files_dir)
        self.savebutton.pack(side=tk.RIGHT)
        savebar.pack(side=tk.BOTTOM, fill=tk.BOTH)

    #TODO initialise dirs

    def add_menubar(self):
        menubar = tk.Menu(self.root_frame)
        sourcemenu = tk.Menu(menubar, tearoff=0)
        dirs = [file for file in os.listdir(self.sitemap_root) if os.path.isdir(os.path.join(self.sitemap_root, file))]
        [sourcemenu.add_radiobutton(label=d, variable=self.selected_sitemap_dir,
                                  command=self.read_sitemap_dir_and_update_progressbar) for d in dirs]
        menubar.add_cascade(label='Bestand', menu=sourcemenu)
        actionmenu = tk.Menu(menubar, tearoff=0)
        actionmenu.add_command(label="Open editor...", command=self.open_editor)
        menubar.add_cascade(label='Bewerken', menu=actionmenu)

        self.selected_sitemap_dir.set(dirs[0])
        self.root.config(menu=menubar)

    def add_progressbar(self):
        self.read_sitemap_dir()
        midbar = ttk.Frame(self.root_frame, height=200)
        self.progressbar_label_text = tk.StringVar(value=f"Site 0 van de {len(self.site_maps)}")
        self.progressbar_label = ttk.Label(midbar, textvariable=self.progressbar_label_text)
        self.progressbar_label.pack(fill=tk.X)
        self.progressbar = ttk.Progressbar(midbar, orient="horizontal", value=0,
                                           maximum=len(self.site_maps))
        self.progressbar.pack(fill=tk.X)
        midbar.pack(fill=tk.X)

    def read_sitemap_dir(self):
        result = []
        for file in os.listdir(os.path.join(self.sitemap_root, self.selected_sitemap_dir.get())):
            if file.lower().endswith('json'):
                result.append(file)
        self.site_maps = result

    def update_progressbar(self):
        self.progressbar['maximum'] = len(self.site_maps)
        self.progressbar_label_text.set(f"Site {self.progressbar['value']} van de {len(self.site_maps)}")

    def read_sitemap_dir_and_update_progressbar(self):
        self.read_sitemap_dir()
        self.update_progressbar()


    @staticmethod
    def open_path(path):
        if platform.system() == "Windows":
            path = path.replace("/", "\\")
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def open_site_map_dir(self):
        self.open_path(os.path.join(self.sitemap_root, self.selected_sitemap_dir.get()))

    def open_saved_files_dir(self):
        self.open_path(self.saved_files_dir)


    def start_crawl(self):
        self.startbutton["state"] = "disabled"
        self.progressbar['value'] = 0
        self.update_progressbar()

        def target(origin):
            controller = scrap.Controller(scraper=self.webcrawler, origin=origin)
            controller.add_dir(os.path.join(self.sitemap_root, self.selected_sitemap_dir.get()))
            controller.start()
            pprint(scrap.Questionnaire.filled_in)

        self.running.append(threading.Thread(target=target, args=[self.remote]).start())

    def open_editor(self):
        pass
        #app = editor.App()
        #app.start()


    def save_crawl(self):
        csvfile = os.path.join('results', f'resultaat_{int(time.time())}.csv')
        header_row = [i for i in scrap.Questionnaire().__dict__.keys()]

        with open(csvfile, "a") as f:
            wr = csv.writer(f, dialect='excel')
            wr.writerow(header_row)
            for result in scrap.Questionnaire.filled_in:
                row = [result.get(i) for i in header_row]
                wr.writerow(row)
        self.open_path(csvfile)

    def remote(self, response):
        self.progressbar['value'] += 1
        self.update_progressbar()
        if self.progressbar['value'] >= len(self.site_maps):
            self.finished()

    def finished(self):
        #self.startbutton["state"] = "enabled"
        self.save_crawl()
        self.restart_app()


    def restart_app(self):
        # since the reactor can't be restarted on its own, the whole app needs to restart
        sys.argv.append('-r')  # from restart
        python = sys.executable
        os.execl(python, python, *sys.argv)  # restart python

    def add_keybinding(self):
        self.root.bind_all('<Return>', None)

    def start(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = App(title="webscraper.py")
    print('Starting...')
    app.start()


