#!/usr/bin/python3
"""This is an experimentation project with Deep Learning
goal: Make a frontend to choose a dataset, explore, tunning the model
and make some predictions

Author: Jose P. Leitao
Date: 2025-01-12
"""

#TODO Define the imports
#TODO Criar a GUI
#DONE Obtain list of datasets
#TODO Create the interface
#DONE list them, so the user can choose the dataset
#DONE list the version, on second colum, in case a dataset has more than one version
#DONE Check the black  background when print the dataset selected
#TODO load the choosed dataset and version
#TODO Display description of Dataset
#TODO Clean the Dataset
#TODO Choose the model
#TODO Training the model
#TODO Make some prediction
#DONE Error message when type on filter box brings no results self.ds_select = item['values'][0]

# Imports
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

#Release number
RELEASE = "0.0.3"

#MACROS


class MyApp(tk.Frame):
    """Main application class"""
    def __init__(self, root):
        self.root = root
        #Define colors
        self.bg_menubar = '#fcfcfc'
        self.fg_menubar = 'BLACK'
        self.active_bg_menubar = '#dedede'
        self.active_fg_menubar = 'BLACK'
        self.bg_menus = '#f3f4f5'
        self.fg_menus = 'BLACK'
        self.active_bg_menus = '#bcdff2'
        self.active_fg_menus = 'BLACK'
        self.bg_app = '#1f1f1f'
        
        super().__init__()
        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.columnconfigure(2, weight=0)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=0)
        self.main_frame.rowconfigure(2, weight=0)
        #self.main_frame.rowconfigure(3, weight=0)

        self.config(background="white", padx=1, pady=1)
                
        self.root.option_add('*tearOff', tk.FALSE)
        self.create_main_menubar()
        

    def my_function(self):
        print('oi')

    def create_main_menubar(self):
        self.mainmenu = tk.Menu(
            self.root,
            background=self.bg_menubar,
            foreground=self.fg_menubar,
            activebackground=self.active_bg_menubar,
            activeforeground=self.active_fg_menubar,
            border=0,
            borderwidth=0,
            activeborderwidth=0,
            font=('Ariel', 10))
        self.root.config(menu=self.mainmenu)

        self.file_menu = tk.Menu(self.mainmenu)
        self.view_menu = tk.Menu(self.mainmenu)
        self.run_menu = tk.Menu(self.mainmenu)
        self.help_menu = tk.Menu(self.mainmenu)

        self.mainmenu.add_cascade(menu=self.file_menu, label='File')
        self.mainmenu.add_cascade(menu=self.view_menu, label='View')
        self.mainmenu.add_cascade(menu=self.run_menu, label='Run')
        self.mainmenu.add_cascade(menu=self.help_menu, label='Help')

        self.add_file_menu_items()
        self.add_view_menu_items()
        self.add_run_menu_items()
        self.add_help_menu_items()

    def add_file_menu_items(self):
        self.file_menu.add_command(label ='Open...', command = self.open_cmd) 
        self.file_menu.add_command(label ='Save', command = None) 
        self.file_menu.add_separator() 
        self.file_menu.add_command(label ='Exit', command = root.destroy)

    def add_view_menu_items(self):
        pass

    def add_run_menu_items(self):
        self.run_menu.add_command(label='Back', command = None, state=tk.DISABLED)
        self.run_menu.add_command(label='Test', command = self.test)

    def add_help_menu_items(self):
        self.help_menu.add_command(label='About', command = self.about)
 
    def about(self):
        messagebox.showinfo(title=None, message=f'Release {RELEASE}')
    
    def test(self):
        print('oi')

    def create_filter(self):
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
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.bind('<<TreeviewSelect>>', self.callback_tree)
        self.tree.grid(row=2, column=0, sticky='nswe')
        
        # define headings
        self.tree.heading('name', text='Name')
        self.tree.heading('version', text='Version')
        self.tree.heading('# of observations', text='# of Observations')

        # All of the items for the listbox.
        #df = self.__load_list__()
        dummy_data = { 'name': ['ds01', 'ds02', 'ds03'],
                      'version': [1, 1, 3],
                      'NumberOfInstances': [100, 200, 300]}
        df = pd.DataFrame(dummy_data)
        self.list_ds = [tuple(r) for r in df[['name', 'version', 'NumberOfInstances']].to_numpy()]
        # add data to the treeview
        for item in self.list_ds:
            self.tree.insert('', tk.END, values=item)

        # The current filter. Setting it to None initially forces the first update.
        self.curr_filter = None
        
        # Test for item selected
        self.test_label = ttk.Label(self.main_frame, text="", background='white',foreground='blue',
                                 font=("Courrier", 16))
        self.test_label.grid(row=3, column=0, columnspan= 3)

        #Create object parameters
        self.ds_selected = ""
        
        # Set the object
        self.__setup__()

    def open_cmd(self):
        self.create_filter()

    # def __load_list__(self):
    #     """Check for csv file and return a Dataframe"""
    #     try:
    #         df = pd.read_csv(OPENML_CSV)
    #     except FileNotFoundError:
    #         openml.config.cache_directory = os.path.expanduser('.')
    #         df = openml.datasets.list_datasets(output_format="dataframe")
    #         df.to_csv(OPENML_CSV, index=False)
    #     return df
    
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
        try:
            self.ds_selected = item['values'][0]
        except:
            self.ds_selected = ''

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


root = tk.Tk()
root.title(f"My Deep Learning Tool - {RELEASE}")
root.geometry('800x600')

myapp = MyApp(root)

myapp.mainloop()



