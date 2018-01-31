import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import time
import sys
import os
import platform
import subprocess
import threading
import csv
import backend.scrap as scrap
import frontend.webscraper as webscraper
from pprint import pprint


class App(webscraper.App):
    def __init__(self, title=""):
        super().__init__()

    def add_topbar(self):
        topbar = ttk.Frame(self.root_frame, height=50)
        l = ttk.Label(topbar, text="Webcrawler Editor", font=("Helvetica", 28))
        l.pack(side=tk.LEFT)
        topbar.pack(side=tk.TOP, fill=tk.X)

    def add_startbar(self):
        startbar = ttk.Frame(self.root_frame)
        self.startbutton = ttk.Button(startbar, text="Start", width=self.button_width, command=self.start_crawl)
        self.startbutton.pack(side=tk.LEFT, pady=10)
        b2 = ttk.Button(startbar, text="Sitemaps", width=self.button_width, command=self.open_site_map_dir)
        b2.pack(side=tk.LEFT, pady=10)
        startbar.pack(side=tk.TOP, fill=tk.X)

    def add_savebar(self):
        savebar = ttk.Frame(self.root_frame)
        self.savebutton = ttk.Button(savebar, text="Resultaten", width=self.button_width, command=self.open_saved_files_dir)
        self.savebutton.pack(side=tk.RIGHT)
        savebar.pack(side=tk.BOTTOM, fill=tk.BOTH)

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

    def start_crawl(self):
        self.startbutton["state"] = "disabled"
        self.progressbar['value'] = 0
        self.update_progressbar()

        def target(origin):
            controller = scrap.Controller(scraper=self.webcrawler, origin=origin)
            controller.add_dir('/'.join([self.sitemap_root, self.selected_sitemap_dir.get()]))
            controller.start()
            pprint(scrap.Questionnaire.filled_in)

        self.running.append(threading.Thread(target=target, args=[self.remote]).start())

    def save_crawl(self):
        csvfile = ''.join(['results/resultaat_', str(int(time.time())), '.csv'])
        header_row = [i for i in scrap.Questionnaire().__dict__.keys()]

        with open(csvfile, "a") as f:
            wr = csv.writer(f, dialect='excel')
            wr.writerow(header_row)
            for result in scrap.Questionnaire.filled_in:
                row = [result.get(i) for i in header_row]
                wr.writerow(row)
        self.open_path(csvfile)


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
    app = App(title="editor.py")
    print('Starting...')
    app.start()


