"""Class definition for Application GUI based on Tkinter"""
import tkinter as tk
from tkinter import ttk

#import openml

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
RELEASE = "0.0.1"


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

        # A listbox with scrollbar for Datasets.   
        self.listbox = tk.Listbox(self, selectmode='single')
        self.listbox.bind('<<ListboxSelect>>', self.callback_listbox)
        self.listbox.grid(row=2, column=0, sticky='nswe')
        yscrollbar = tk.Scrollbar(self, orient='vertical')
        yscrollbar.grid(row=2, column=1, sticky='ns')
        yscrollbar.config(command=self.listbox.yview)
       
        # All of the items for the listbox.
        df = pd.read_csv(OPENML_CSV)
        self.items = df['name'].iloc[0:MAX_DS].to_list()

        # The current filter. Setting it to None initially forces the first update.
        self.curr_filter = None
        
        # Test of List_ds
        self.test_label = ttk.Label(text="", foreground='blue',
                                     background="white", font=("Courrier", 16))
        self.test_label.grid(row=3, column=0, columnspan=3)
        #End of UI definition
        
        #Create object parameters
        self.ds_selected = ""
        
        # Set the object
        self.__setup__()

    def __setup__(self):
        # The initial update.
        self.on_tick()
        
    def callback_listbox(self, event):
        """Callback function when a dataset is select"""
        #There is no use for 'event' received, but just to clear the message from pylint
        if event:
            event = None
        #self.ds_selected = self.items[self.listbox.curselection()[0]]
        self.ds_selected = self.listbox.get(self.listbox.curselection()[0])
        # teste
        self.test_label.config(text=self.ds_selected)
        
    def on_tick(self):
        if self.filter_box.get() != self.curr_filter:
            # The contents of the filter box has changed.
            self.curr_filter = self.filter_box.get()

            # Refresh the listbox.
            self.listbox.delete(0, 'end')
            for item in self.items:
                if self.curr_filter in item:
                    self.listbox.insert('end', item)
        self.after(250, self.on_tick)
    