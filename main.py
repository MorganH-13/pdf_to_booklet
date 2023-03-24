from PyPDF2 import PdfReader, PdfWriter
from new_pdf_gen import NewPDF
from gui import Gui


def create_new_pdf(name: str):
    NewPDF(name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gui = Gui()
    # create_new_pdf('sample.pdf')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
