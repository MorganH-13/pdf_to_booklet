from PyPDF2 import PdfReader, PdfWriter
from new_pdf_gen import NewPDF
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk, filedialog as fd


class Gui:
    def __init__(self):
        self.file_path = None
        self.file_name = None
        root = tk.Tk()
        root.title('Select File')
        root.geometry('700x350')

        button = tk.Button(
            root,
            text='Select File',
            command=self.file_select
                           )
        button.pack(expand=True)
        root.mainloop()

    def file_select(self):
        self.file_path = fd.askopenfilename(
            filetypes=(('PDF File', '*.pdf'),
                       ('All Files', '*.*'))
        )
        self.file_name = self.file_path.split('/')[-1]
        showinfo(
            title='Selected File',
            message=self.file_name
        )


def create_new_pdf(name: str):
    NewPDF(name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gui = Gui()
    create_new_pdf('sample.pdf')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
