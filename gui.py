import math
import tkinter as tk
from tkinter import ttk, filedialog as fd
from new_pdf_gen import NewPDF
from book import Book


class Gui:
    def __init__(self):
        self.book = None
        self.newPDF = None
        self.valid = True

        self.root = tk.Tk()
        self.root.title('Select File')
        self.root.geometry('700x350')
        self.root.resizable(False, False)

        self.build_gui()
        self.root.mainloop()

    def build_gui(self):
        self.build_input()
        self.sign_info()
        self.print_options()
        self.build_generator()

    def build_input(self):
        w = 200
        h = 150
        section = tk.Frame(self.root, bg='lightgrey', width=w, height=h)
        section.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        section.grid_propagate(False)
        section.grid_rowconfigure(1, weight=1)
        section.grid_columnconfigure(0, weight=1)

        # Section widgets building
        title = tk.Label(section, text='Input File', bg='lightgrey')
        inputFrame = tk.LabelFrame(section, bg='lightgrey')
        button = tk.Button(section, bg='lightgrey', text='Select File',
                           command=lambda: [self.file_select()])

        # Input Frame info labels
        self.file = tk.Label(inputFrame, bg='lightgrey', text='No File Selected',
                             anchor='w')
        self.length = tk.Label(inputFrame, bg='lightgrey', anchor='w')
        self.size = tk.Label(inputFrame, bg='lightgrey', anchor='w')

        # Aligning section pieces
        title.grid(row=0, column=0)
        inputFrame.grid(row=1, column=0, padx=(5, 5), sticky='ew')
        button.grid(row=2, column=0, pady=(5, 5))

        # Inside InputFrame
        self.file.grid(row=0, column=0, sticky='w')
        self.length.grid(row=1, column=0, sticky='w')
        self.size.grid(row=2, column=0, sticky='w')

    def sign_info(self):
        w = 200
        h = 130
        self.root.grid_columnconfigure(1, weight=1)
        section = tk.Frame(self.root, bg='lightgrey', width=w, height=h)
        section.grid(row=0, column=2, sticky='ne', padx=(5, 5), pady=(5, 5))
        section.grid_propagate(False)
        section.grid_rowconfigure(1, weight=1)
        section.grid_columnconfigure(0, weight=1)

        # Section widget building
        title = tk.Label(section, bg='lightgrey', text='Signature Info')
        signatureFrame = tk.LabelFrame(section, bg='lightgrey')

        # Signature Frame info labels
        signatureAsk = tk.Label(signatureFrame, bg='lightgrey',
                                text='Sheets per signature:')
        self.signatureLength = ttk.Entry(signatureFrame, width=3)
        self.signatureLength.insert(0, '1')
        self.signatureLength.bind('<KeyRelease>', self.update_signatures)
        self.signatureCount = tk.Label(signatureFrame, bg='lightgrey',
                                       text='No sections generated')
        self.sheetCount = tk.Label(signatureFrame, bg='lightgrey')

        # Aligning section pieces
        title.grid(row=0, column=0)
        signatureFrame.grid(row=1, column=0, sticky='ew', padx=(5, 5))

        # Inside SignatureFrame
        signatureAsk.grid(row=0, column=0, sticky='w')
        self.signatureLength.grid(row=0, column=1, sticky='w')
        self.signatureCount.grid(row=1, column=0, columnspan=2, sticky='w')
        self.sheetCount.grid(row=2, column=0, columnspan=2, sticky='w')

    def print_options(self):
        w = 200
        h = 130
        section = tk.Frame(self.root, bg='lightgrey', width=w, height=h)
        section.grid(row=0, column=1, sticky='n', padx=(5, 5), pady=(5, 5))
        section.grid_propagate(False)
        section.grid_rowconfigure(1, weight=1)
        section.grid_columnconfigure(0, weight=1)

        # Section widget building
        title = tk.Label(section, bg='lightgrey', text='Printer Options')
        printerFrame = tk.LabelFrame(section, bg='lightgrey')

        # Printer Frame selections
        choices = {'A4', 'Legal'}
        paperSize = tk.Label(printerFrame, bg='lightgrey', text='Paper Size')
        self.dropdown = tk.StringVar(printerFrame)
        self.dropdown.set('A4')
        menu = tk.OptionMenu(printerFrame, self.dropdown, *choices)
        pagesAsk = tk.Label(printerFrame, bg='lightgrey',
                            text='Pages per face:')
        self.pagesPer = ttk.Entry(printerFrame, width=3)
        self.pagesPer.insert(0, '2')
        self.pagesPer.bind('<KeyRelease>', self.update_signatures)

        # Aligning section pieces
        title.grid(row=0, column=0)
        printerFrame.grid(row=1, column=0, sticky='ew', padx=(5, 5))

        # Inside PrinterFrame
        paperSize.grid(row=0, column=0)
        menu.grid(row=0, column=1)
        pagesAsk.grid(row=1, column=0)
        self.pagesPer.grid(row=1, column=1)

    def build_generator(self):
        w = 200
        h = 130
        section = tk.Frame(self.root, bg='lightgrey', width=w, height=h)
        section.grid(row=1, column=1)

        # Section widget building
        confirmButton = tk.Button(section, bg='lightgrey',
                                  text='Save PDF Docs')
        self.display = tk.Label(section, bg='lightgrey')

    def file_select(self):
        try:
            if self.book:
                del self.book
            path = fd.askopenfilename(
                filetypes=(('PDF File', '*.pdf'),
                           ('All Files', '*.*'))
            )
            self.book = Book(path)
            self.update_input()
            self.update_signatures()

        finally:
            pass

    def update_input(self):
        self.file.configure(anchor='w', text=self.book.name, justify=tk.LEFT)
        self.length.configure(anchor='w', text='No. of Pages: %s' %
                              str(self.book.length), justify=tk.LEFT)
        self.size.configure(anchor='w', text='Page Size: %sx%s' %
                            (self.book.height, self.book.width), justify=tk.LEFT)

    def update_signatures(self, *args):
        if self.book:
            sigSize = self.signatureLength.get()
            pages = self.pagesPer.get()
            if sigSize == '':
                return
            if pages == '':
                return
            try:
                self.book.pagesPer = int(pages)
                self.book.update()
                count = float(self.book.length) / (int(sigSize)*4)
                count = int(math.floor(count))
                remainder = self.book.length % (int(sigSize)*4)
                self.signatureCount.configure(text='%s signatures and %s sheet(s)' %
                                                   (count, remainder))
                self.sheetCount.configure(text='%s total sheets' % self.book.sheets)
                self.book.signatures = count
                self.book.extraPages = remainder
            except ValueError:
                self.valid = False
                pass
