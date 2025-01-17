#!/usr/bin/python3
"""This is an experimentation project with Deep Learning
goal: Make a frontend to choose a dataset, explore, tunning the model
and make some predictions

Author: Jose P. Leitao
Date: 2025-01-17
"""

#TODO Define the imports
#TODO Criar a GUI
#DONE (R-0.0.3) obtain list of datasets
#TODO Create the interface
#DONE (R-0.0.3) list them, so the user can choose the dataset
#DONE (R-0.0.3) list the version, on second colum, in case a dataset has more than one version
#DONE (R-0.0.3) Check the black background when print the dataset selected
#FIXME create option to select the source (OpenML or Kaggle)
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
RELEASE = "0.0.4"

#MACROS


class MyApp(tk.Frame):
    """Main application class"""
    def __init__(self, root):
        self.root = root
        super().__init__()
        self.root.option_add('*tearOff', tk.FALSE)

        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.columnconfigure(2, weight=0)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=0)
        self.main_frame.rowconfigure(2, weight=0)

        self.create_main_menubar()
        self.create_extra_frames()

    def create_main_menubar(self):
        self.mainmenu = tk.Menu(self.root)
        self.root.config(menu=self.mainmenu)
        self.file_menu = tk.Menu(self.mainmenu)
        self.preference_menu = tk.Menu(self.mainmenu)
        self.view_menu = tk.Menu(self.mainmenu)
        self.run_menu = tk.Menu(self.mainmenu)
        self.help_menu = tk.Menu(self.mainmenu)

        self.mainmenu.add_cascade(menu=self.file_menu, label='File')
        self.mainmenu.add_cascade(menu=self.preference_menu, label='Preference')
        self.mainmenu.add_cascade(menu=self.view_menu, label='View')
        self.mainmenu.add_cascade(menu=self.run_menu, label='Run')
        self.mainmenu.add_cascade(menu=self.help_menu, label='Help')

        self.add_file_menu_items()
        self.add_preference_menu_items()
        self.add_view_menu_items()
        self.add_run_menu_items()
        self.add_help_menu_items()
    
    def create_extra_frames(self):
        self.fr_work = tk.Frame(self.main_frame, height=570, background='pink')
        self.fr_work.grid_propagate(False)
        self.fr_work.grid(row=1, column=0, sticky='nswe')
        self.fr_status = tk.Frame(self.main_frame, height=30, background='white')
        self.fr_status.grid_propagate(False)
        self.fr_status.grid(row=2, column=0, sticky='nswe')

    def add_file_menu_items(self):
        self.file_menu.add_command(label ='Open...', command = self.open_command) 
        self.file_menu.add_command(label ='Save', command = None) 
        self.file_menu.add_separator() 
        self.file_menu.add_command(label ='Exit', command = root.destroy)

    def add_preference_menu_items(self):
        self.preference_menu.add_command(label ='Set Source', command = self.set_source_cmd)  

    def add_view_menu_items(self):
        pass
        
    def add_run_menu_items(self):
        self.run_menu.add_command(label='Back', command = None, state=tk.DISABLED)
        self.run_menu.add_command(label='Test', command = self.test)

    def add_help_menu_items(self):
        self.help_menu.add_command(label='About', command = self.about)

    def set_source_cmd(self):
        self.clear_frame(self.fr_work)
        lbl_source = tk.Label(self.fr_work, text='Set Source')
        lbl_source.grid(row=0, column=0)
      
    def clear_frame(self, frame):
        """Clear all widgets from a frame"""
        for child in frame.winfo_children():
            child.destroy()

    def about(self):
        messagebox.showinfo(title=None, message=f'Release {RELEASE}')

    def open_command(self):
        self.clear_frame(self.fr_work)
        # Put the filter label and entry box in the frame.
        tk.Label(self.fr_work, text='Filter:').grid(row=0, column=0, sticky='w' )
        self.filter_box = tk.Entry(self.fr_work, width=95)
        self.filter_box.grid(row=0, column=0, padx=40, sticky='e')
     
        # A tree with multiple columns
        # define columns
        columns = ('name', 'version', '# of observations')
        self.tree = ttk.Treeview(self.fr_work, columns=columns, show='headings', selectmode='browse')
        self.tree.bind('<<TreeviewSelect>>', self.callback_tree)
        self.tree.grid(row=1, column=0, sticky='nswe')
        
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
        self.test_label = ttk.Label(self.fr_status, text="", background='white',foreground='blue',
                                font=("Courrier", 12))
        self.test_label.grid(row=0, column=0, padx=400)

        #Create object parameters
        self.ds_selected = ""

        # Set the object
        self.__setup__()

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
        try:
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
        except:
            pass    

    
    def test(self):
        #print('oi')
        self.clear_frame(self.fr_work)
        lbl_test = tk.Label(self.fr_work, text='TEST')
        lbl_test.grid(row=0, column=0)         
        
### main() ###
root = tk.Tk()
root.title(f"My Deep Learning Tool - {RELEASE}")
root.geometry('800x600')
root.resizable(False, False)

myapp = MyApp(root)

myapp.mainloop()



