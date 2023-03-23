from book import Book
import tkinter as tk
from tkinter import ttk, filedialog as fd

class Gui:
    def __init__(self):
        self.book = Book()

        self.root = tk.Tk()
        self.root.title('Select File')
        self.root.geometry('700x350')
        self.root.resizable(False, False)

        self.build_gui()
        self.root.mainloop()

    def build_gui(self):
        self.build_input()

    def build_input(self):
        w = 200
        h = 150
        self.section = tk.Frame(self.root, bg='lightgrey', width=w, height=h)
        title = tk.Label(self.section, text='Input File', bg='lightgrey')
        inputFrame = tk.LabelFrame(self.section, bg='lightgrey')
        self.file = tk.Label(inputFrame, bg='lightgrey', text='No File Selected')
        button = tk.Button(self.section, bg='lightgrey', text='Select File',
                           command=lambda: [self.file_select()])
        self.length = tk.Label(inputFrame, bg='lightgrey')
        self.size = tk.Label(inputFrame, bg='lightgrey')

        self.section.pack(side=tk.LEFT, padx=(10, 10), pady=(10, 10), anchor='n')
        self.section.pack_propagate(False)
        title.pack(side=tk.TOP)
        button.pack(side=tk.BOTTOM, pady=(5, 5))
        inputFrame.pack(side=tk.BOTTOM, expand=True, fill='both',
                        padx=(5, 5))
        self.file.pack()

    def file_select(self):
        try:
            path = fd.askopenfilename(
                filetypes=(('PDF File', '*.pdf'),
                           ('All Files', '*.*'))
            )
            self.book.read_in(path)
            self.update_info()
        finally:
            pass

    def update_info(self):
        self.file.configure(anchor='w', text=self.book.name, justify=tk.LEFT)
        self.length.configure(anchor='w', text='No. of Pages: %s' %
                              str(self.book.length), justify=tk.LEFT)
        self.size.configure(anchor='w', text='Page Size: %sx%s' %
                            (self.book.height, self.book.width), justify=tk.LEFT)

        self.file.pack(side=tk.TOP, fill='x')
        self.length.pack(side=tk.TOP, fill='x')
        self.size.pack(side=tk.TOP, fill='x')
