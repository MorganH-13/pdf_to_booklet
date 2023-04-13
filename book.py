from PyPDF2 import PdfReader, PdfWriter, PaperSize
import math

class Book:
    def __init__(self, path: str):
        self.path = path
        self.name = self.path.split('/')[-1]
        # self.pdf = open(self.path, 'rb')
        self.pdfReader = PdfReader(self.path)
        self.length = len(self.pdfReader.pages)
        self.width = PaperSize.A4.width
        self.height = PaperSize.A4.height
        self.pagesPer = 2  # Pages per face
        self.sheets = math.ceil(self.length/(2*self.pagesPer))

        self.signatures = 0
        self.sigSize = 0
        self.extraPages = 0

        self.sig_front = None
        self.sig_back = None
        self.specialSig = False

    def update(self):
        self.sheets = math.ceil(self.length/(2*self.pagesPer))

    def set_signatures(self, front: [], back: []):
        self.sig_front = front[:]
        self.sig_back = back[:]
