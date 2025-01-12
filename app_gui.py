"""Class definition for Application GUI based on Tkinter"""
import os
import tkinter as tk
from tkinter import ttk

import openml

import pandas as pd

#from sklearn.datasets import fetch_openml

#from random import randrange

#from collections import deque

#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.figure import Figure

#Constants
BLACK = "#000000"
RED = "#e7305b"
GREEN = "#55ff33"
WIN_WIDTH = 800
WIN_HEIGHT = 600
OPENML_CSV = 'openml_datasets.csv'
MAX_DS = 4000

#Release number
RELEASE = "0.0.2"


class App(tk.Tk):
    """Class for Application GUI"""
    def __init__(self):
        super().__init__()
        #main window
        self.title(f"My Deep Learning Tool - {RELEASE}")
        self.geometry('800x600')
        self.minsize(width=WIN_WIDTH, height=WIN_HEIGHT)
        #self.maxsize(width=WIN_WIDTH, height=WIN_HEIGHT)
        self.config(background="white", padx=1, pady=1)

        # 4 rows x 3 columns grid.
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        #Title
        self.title_label = ttk.Label(text="My Deep Learning Tool", foreground=BLACK,
                                     background="white", font=("Courrier", 16))
        self.title_label.grid(row=0, column=0, columnspan=3)

        # Put the filter in a frame at the top spanning across the columns.
        frame = tk.Frame(self)
        frame.grid(row=1, column=0, columnspan=2, sticky='we')

        # Put the filter label and entry box in the frame.
        tk.Label(frame, text='Filter:').pack(side='left')

        self.filter_box = tk.Entry(frame)
        self.filter_box.pack(side='left', fill='x', expand=True)

        # A tree with multiple columns
        # define columns
        columns = ('name', 'version', '# of observations')
        self.tree = ttk.Treeview(columns=columns, show='headings', selectmode='browse')
        self.tree.bind('<<TreeviewSelect>>', self.callback_tree)
        self.tree.grid(row=2, column=0, sticky='nswe')

        # define headings
        self.tree.heading('name', text='Name')
        self.tree.heading('version', text='Version')
        self.tree.heading('# of observations', text='# of Observations')

        # All of the items for the listbox.
        df = self.__load_list__()
        self.list_ds = [tuple(r) for r in df[['name', 'version', 'NumberOfInstances']].to_numpy()]
        # add data to the treeview
        for item in self.list_ds:
            self.tree.insert('', tk.END, values=item)

        # The current filter. Setting it to None initially forces the first update.
        self.curr_filter = None
        
        # Test for item selected
        self.test_label = ttk.Label(text="", foreground='blue',
                                     background="white", font=("Courrier", 16))
        self.test_label.grid(row=3, column=0, columnspan=3)
        #End of UI definition
        
        #Create object parameters
        self.ds_selected = ""
        
        # Set the object
        self.__setup__()

    def __load_list__(self):
        """Check for csv file and return a Dataframe"""
        try:
            df = pd.read_csv(OPENML_CSV)
        except FileNotFoundError:
            openml.config.cache_directory = os.path.expanduser('.')
            df = openml.datasets.list_datasets(output_format="dataframe")
            df.to_csv(OPENML_CSV, index=False)
        return df
    
    def __setup__(self):
        # The initial update.
        self.on_tick()

    def callback_tree(self, event):
        """Callback function when a dataset is select"""
        #There is no use for 'event' received, but just to clear the message from pylint
        if event:
            event = None
        selected_item = self.tree.selection()
        item = self.tree.item(selected_item)
        self.ds_selected = item['values'][0]
        # teste
        self.test_label.config(text=self.ds_selected)
        
    def on_tick(self):
        if self.filter_box.get() != self.curr_filter:
            # The contents of the filter box has changed.
            self.curr_filter = self.filter_box.get()

            # Refresh the treeview.
            for item in self.tree.get_children():
                self.tree.delete(item)
            for item in self.list_ds:
                if self.curr_filter in str(item[0]):
                    self.tree.insert('', tk.END, values=item)
        self.after(250, self.on_tick)
