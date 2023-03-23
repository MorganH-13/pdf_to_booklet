from PyPDF2 import PdfReader, PdfWriter


class Book:
    def __init__(self):
        self.name      = None
        self.length     = None
        self.width     = None
        self.height    = None
        self.path      = None
        self.pdf       = None
        self.pdfReader = None

    def read_in(self, path):
        self.path = path
        self.name = self.path.split('/')[-1]
        self.pdf = open(self.path, 'rb')
        self.pdfReader = PdfReader(self.pdf)
        self.length = len(self.pdfReader.pages)
        self.width = self.pdfReader.pages[0].mediabox.width
        self.height = self.pdfReader.pages[0].mediabox.height
        print(self.height)
        print(self.width)
