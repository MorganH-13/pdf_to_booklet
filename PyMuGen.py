import math
import copy
from time import time
from book import Book
import fitz
class Formatter:
    def __init__(self, book: Book):
        self.book = book
        self.input = fitz.open(self.book.path)

        self.book.specialSig = False
        self.big_sig = False
        self.front_list = []
        self.back_list = []
        self.gutter = 75

        self.standard_width = (self.book.height-self.gutter)/2
        self.standard_height = self.book.width

        self.build_signature_list()
        print(self.front_list)
        print(self.back_list)

    def build_signature_list(self):
        if self.book.extraPages > 0:
            self.book.specialSig = True
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
                signature_front.append(start + j - 1)
                signature_front.append(end - j - 1)
                # Prepend
                # (end + 1 - j, start - 1 + j)
                signature_back.insert(0, end + 1 - j - 1)
                signature_back.insert(1, (start - 1 + j - 1))
                j += 2
            start = end + 1
            self.front_list.append(signature_front)
            self.back_list.insert(0, signature_back)

        if self.book.specialSig:
            added_sheets = math.ceil(self.book.extraPages / 4)
            if self.big_sig:
                sig_len = self.book.sigSize + added_sheets
            else:
                sig_len = added_sheets

            length = sig_len * 4
            signature_front = []
            signature_back = []
            end = end + (4 * sig_len)
            j = 1
            while j < length / 2:
                signature_front.append(start + j - 1)
                signature_front.append(end - j - 1)
                signature_back.insert(0, end - j)
                signature_back.insert(1, (start + j - 2))
                j += 2
            self.front_list.append(signature_front)
            self.back_list.insert(0, signature_back)

    def format_pdf(self):
        self.formatted = fitz.Document()
        self.format_front()
        if self.book.specialSig:
            self.special_front()
        if self.book.pagesPer == 4:
            self.double_up_front()
        self.formatted.save('intermediate_front.pdf', garbage=3, deflate=True)

        self.formatted = fitz.Document()
        if self.book.specialSig:
            self.special_back()
        self.format_back()
        if self.book.pagesPer == 4:
            self.double_up_back()
        self.formatted.save('intermediate_back.pdf', garbage=3, deflate=True)

    def format_front(self):
        loop = len(self.front_list)
        if self.book.specialSig:
            loop -= 1

        i = 0
        while i < loop:
            self.signature_loop(self.front_list[i])
            i += 1

    def format_back(self):
        i = 0
        loop = len(self.back_list)
        if self.book.specialSig:
            i = 1

        while i < loop:
            self.signature_loop(self.back_list[i])
            i += 1

    def special_front(self):
        self.signature_loop(self.front_list[-1])

    def special_back(self):
        self.signature_loop(self.back_list[0])

    def signature_loop(self, signature: []):
        j = 0
        while j < len(signature):
            self.page_merge(signature, j)
            j += 2

    def page_merge(self, signature: [], j: int):
        left_page = fitz.Rect(0, 0,
                              self.standard_width, self.standard_height)
        right_page = fitz.Rect(self.standard_width + self.gutter, 0,
                               (self.standard_width * 2) + self.gutter,
                               self.standard_height)

        page_base = self.formatted.new_page(-1,
                                            width=(self.standard_width * 2) + self.gutter,
                                            height=self.standard_height)

        if signature[j] < self.book.length:
            page_base.show_pdf_page(left_page,
                                    self.input,
                                    signature[j],
                                    keep_proportion=False)
        if signature[j + 1] < self.book.length:
            page_base.show_pdf_page(right_page,
                                    self.input,
                                    signature[j+1],
                                    keep_proportion=False)

    def double_up_front(self):
        i = 0
        doubled_sheet = fitz.Document()

        while i < len(self.formatted):
            top_page = fitz.Rect(0, 0,
                                 self.book.width, self.book.height/2)
            bottom_page = fitz.Rect(0, self.book.height/2,
                                    self.book.width, self.book.height)

            page_base = doubled_sheet.new_page(-1,
                                               width=self.book.width,
                                               height=self.book.height)

            if self.formatted[i].get_contents():
                page_base.show_pdf_page(top_page,
                                        self.formatted,
                                        i,
                                        keep_proportion=False)
            if i + 1 < len(self.formatted):
                if self.formatted[i + 1].get_contents():
                    page_base.show_pdf_page(bottom_page,
                                            self.formatted,
                                            i + 1,
                                            keep_proportion=False)

            i += 2
        self.formatted = doubled_sheet

    def double_up_back(self):
        i = len(self.formatted) - 1
        doubled_sheet = fitz.Document()

        while i >= 0:
            top_page = fitz.Rect(0, 0,
                                 self.book.width, self.book.height/2)
            bottom_page = fitz.Rect(0, self.book.height/2,
                                    self.book.width, self.book.height)

            page_base = doubled_sheet.new_page(0,
                                               width=self.book.width,
                                               height=self.book.height)

            if self.formatted[i].get_contents():
                page_base.show_pdf_page(top_page,
                                        self.formatted,
                                        i,
                                        keep_proportion=False)
                if i - 1 < len(self.formatted):
                    if self.formatted[i - 1].get_contents():
                        page_base.show_pdf_page(bottom_page,
                                                self.formatted,
                                                i - 1,
                                                keep_proportion=False)

            i -= 2
        self.formatted = doubled_sheet
