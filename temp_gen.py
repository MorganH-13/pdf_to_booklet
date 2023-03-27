import math
from book import Book
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PyPDF2 import PageObject


class PDF:
    def __init__(self, book: Book):
        self.book = book
        self.special_sig = False
        self.big_sig = False

        self.front_list = []
        self.back_list = []

        self.front_pdf = "front.pdf"
        self.back_pdf = "back.pdf"
        self.pdf_writer_front = PdfWriter()
        self.pdf_writer_back = PdfWriter()

        self.build_signature_list()
        self.book.set_signatures(self.front_list, self.back_list)

    def build_signature_list(self):
        if self.book.extraPages > 0:
            self.special_sig = True
            if self.book.extraPages <= 4:
                self.book.signatures -= 1
                self.big_sig = True

        length = self.book.sigSize * 4
        start = 1
        end = 0
        for i in range(self.book.signatures):
            signature_front = []
            signature_back = []
            end = 4 * self.book.sigSize * (i + 1)
            j = 1
            while j < length / 2:
                # Append
                # (start + j, end - j)
                signature_front.append(start + j)
                signature_front.append(end - j)
                # Prepend
                # (end + 1 - j, start - 1 + j)
                signature_back.append(end + 1 - j)
                signature_back.append(start - 1 + j)
                j += 2
            start = end + 1
            self.front_list.append(signature_front)
            self.back_list.append(signature_back)

        if self.special_sig:
            addedSheets = math.ceil(self.book.extraPages / 4)
            if self.big_sig:
                sig_len = self.book.sigSize + addedSheets
            else:
                sig_len = addedSheets

            length = sig_len * 4
            signature_front = []
            signature_back = []
            end = end + (4 * sig_len)
            j = 1
            while j < length / 2:
                signature_front.append(start + j)
                signature_front.append(end - j)
                signature_back.append(end + 1 - j)
                signature_back.append(start - 1 + j)
                j += 2
            self.front_list.append(signature_front)
            self.back_list.append(signature_back)
