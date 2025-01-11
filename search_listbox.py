import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Example of a filtered listbox')

        # Full screen.
        self.state('normal')

        # 3 rows x 2 columns grid.
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # Put the filter in a frame at the top spanning across the columns.
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, columnspan=2, sticky='we')

        # Put the filter label and entry box in the frame.
        tk.Label(frame, text='Filter:').pack(side='left')

        self.filter_box = tk.Entry(frame)
        self.filter_box.pack(side='left', fill='x', expand=True)

        # A listbox with scrollbars.
        yscrollbar = tk.Scrollbar(self, orient='vertical')
        yscrollbar.grid(row=1, column=1, sticky='ns')

        xscrollbar = tk.Scrollbar(self, orient='horizontal')
        xscrollbar.grid(row=2, column=0, sticky='we')

        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=1, column=0, sticky='nswe')

        yscrollbar.config(command=self.listbox.yview)
        xscrollbar.config(command=self.listbox.xview)

        # The current filter. Setting it to None initially forces the first update.
        self.curr_filter = None

        # All of the items for the listbox.
        self.items = [str(i) for i in range(100)]

        # The initial update.
        self.on_tick()

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

App().mainloop()