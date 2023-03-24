from PyPDF2 import PdfReader, PdfWriter
import math

class Book:
    def __init__(self, path: str):
        self.path = path
        self.name = self.path.split('/')[-1]
        self.pdf = open(self.path, 'rb')
        self.pdfReader = PdfReader(self.pdf)
        self.length = len(self.pdfReader.pages)
        self.width = self.pdfReader.pages[0].mediabox.width
        self.height = self.pdfReader.pages[0].mediabox.height
        self.pagesPer = 2  # Pages per face
        self.sheets = int(math.ceil(self.length/(2*self.pagesPer)))

        self.signatures = 0
        self.extraPages = 0

    def update(self):
        self.sheets = int(math.ceil(self.length/(2*self.pagesPer)))

