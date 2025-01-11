"""Class definition for Application GUI based on Tkinter"""
import tkinter as tk
from tkinter import ttk

import openml

from sklearn.datasets import fetch_openml

#from random import randrange

#from collections import deque

#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.figure import Figure

#Constants
BLACK = "#000000"
RED = "#e7305b"
GREEN = "#55ff33"
FONT_NAME = "Ariel"
WIN_WIDTH = 800
WIN_HEIGHT = 600
LIST_DS = ['DS01', 'DS02', 'DS03']

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
        #Title
        self.title_label = ttk.Label(text="My Deep Learning Tool", foreground=BLACK,
                                     background="white", font=("Courrier", 16))
        self.title_label.place(relx=0.35)
        
        #List Box with Dataset
        self.list_box_ds = tk.Listbox(height=1, width=25, selectmode='single')
        self.list_box_ds.bind('<<ListboxSelect>>', self.callback_list_ds)
        self.list_box_ds.place(relx=0, rely=0.1)
        #Include a yscrollbar besides the listbox
        self.list_scrollbar = tk.Scrollbar(orient='vertical', width=10)
        self.list_scrollbar.place(relx=0.25, rely=0.1)
        #Attach scrollbar to listbox
        self.list_box_ds.config(yscrollcommand= self.list_scrollbar.set)
        self.list_scrollbar.config(command = self.list_box_ds.yview)
        
        #DS Label
        self.ds_label = ttk.Label(text="List of Datasets:", background="white",foreground="black",
                                    font=("Arial",8))
        self.ds_label.place(relx=0, rely=0.07)
        
        # Test of List_ds
        self.test_label = ttk.Label(text="", foreground='blue',
                                     background="white", font=("Courrier", 16))
        self.test_label.place(relx=0.5, rely=0.5)
        #End of UI definition
        #Create object parameters
        self.ds_selected = ""
        
        #Read Button
        #self.read_button = ttk.Button(text="", command=self.start_stop_read)
        #self.read_button.grid(column=2, row=1)
        #Canvas
        # self.canvas = tk.Canvas(width=150, height=40, background=BLACK, highlightthickness=0)
        # self.read_text = self.canvas.create_text(80, 20, fill=GREEN, text="", font=(FONT_NAME, 18))
        # self.canvas.grid(column=1, row=1,pady=0)
        #Figure that will contain the plot
        # self.fig = Figure(figsize = (3, 2), dpi = 100)
        # self.ax = self.fig.add_subplot(1, 1, 1)
        # self.ax.set_facecolor('black')
        # self.ax.grid(visible=True, which='both',linestyle='dotted')
        # self.ax.set_ylim(-80,20)
        # self.ax.tick_params(axis='both',labelsize=6)
        # self.ax.set_xlim(60, 0)
        # self.ax.yaxis.tick_right()
        # self.fig.canvas.draw()
        #Create a canvas to contains the figure
        # self.canvas_fig = FigureCanvasTkAgg(self.fig)
        # self.canvas_fig.get_tk_widget().configure(width=200,height=70)
        # self.canvas_fig.get_tk_widget().grid(column=1, row=2, pady= 0, ipadx=40,
        #                                      ipady=40, sticky='N')
        # Set the object
        self.__setup__()

    def __setup__(self):
        #Fill List of Datasets
        for ds in LIST_DS:
            self.list_ds.insert(tk.END, ds)
        

    def callback_list_ds(self, event):
        """Callback function when a dataset is select"""
        #There is no use for 'event' received, but just to clear the message from pylint
        if event:
            event = None
        self.ds_selected = LIST_DS[self.list_ds.curselection()[0]]
        # teste
        self.test_label.config(text=self.ds_selected)
        

    

    def plot(self, y_list):
        """Plot the store reading"""
        #clear any previous plot and plot with new data
        self.ax.cla()
        self.ax.grid(visible=True, which='both',linestyle='dotted')
        self.ax.set_ylim(-80,20)
        self.ax.tick_params(axis='both',labelsize=6)
        self.ax.set_xlim(60, 0)
        self.ax.yaxis.tick_right()
        self.ax.plot(self.x_data, y_list, color='orange', linewidth=1.5)
        self.fig.canvas.draw()
        