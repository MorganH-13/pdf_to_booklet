import math
import copy
from time import time

import PyPDF2
from book import Book
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PyPDF2 import PageObject
from PyPDF2.generic import RectangleObject


class PDF:
    def __init__(self, book: Book):
        self.book = book
        self.book.specialSig = False
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
                signature_front.append(start + j -1)
                signature_front.append(end - j -1)
                # Prepend
                # (end + 1 - j, start - 1 + j)
                signature_back.insert(0, end + 1 - j - 1)
                signature_back.insert(1, (start - 1 + j - 1))
                j += 2
            start = end + 1
            self.front_list.append(signature_front)
            self.back_list.insert(0, signature_back)

        if self.book.specialSig:
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
                signature_front.append(start + j -1)
                signature_front.append(end - j -1)
                signature_back.insert(0, end + 1 - j -1)
                signature_back.insert(1, (start - 1 + j -1))
                j += 2
            self.front_list.append(signature_front)
            self.back_list.insert(0, signature_back)

    def format_pdf(self):
        self.format_front(self.front_list)
        # self.format_back(self.back_list)

        # if self.book.specialSig:
        #     self.special_front(self.front_list[-1])
        #     self.special_back(self.back_list[0])

        # if self.book.pagesPer == 4:
        #     self.double_print()

        with open('out_front.pdf', 'wb') as out_front:
            self.pdf_writer_front.write(out_front)
        # with open('out_back.pdf', 'wb') as out_back:
        #     self.pdf_writer_back.write(out_back)

    def format_front(self, front: []):
        loop = len(front)
        if self.book.specialSig:
            loop -= 1

        i = 0
        while i < loop:
            signature = front[i]
            j = 0
            while j < len(signature):
                page1 = self.book.pdfReader.pages[signature[j]]
                page2 = self.book.pdfReader.pages[signature[j + 1]]
                merged_page = self.merge_page_2(copy.copy(page1), copy.copy(page2))

                self.pdf_writer_front.add_page(merged_page)
                j += 2
            i += 1

    def format_back(self, back: []):
        i = 0
        loop = len(back)
        if self.book.specialSig:
            i = 1

        while i < loop:
            signature = back[i]
            j = 0
            while j < len(signature):
                page1 = self.book.pdfReader.pages[signature[j]]
                page2 = self.book.pdfReader.pages[signature[j + 1]]
                merged_page = self.merge_page_2(copy.copy(page1), copy.copy(page2))

                self.pdf_writer_back.add_page(merged_page)
                j += 2
            i += 1

    def special_front(self, front: []):
        j = 0
        page1 = PageObject.create_blank_page(None, self.book.width,
                                             self.book.height)
        page2 = PageObject.create_blank_page(None, self.book.width,
                                             self.book.height)

        while j < len(front):
            if front[j] < self.book.length:
                page1 = self.book.pdfReader.pages[front[j]]
            if (j + 1 < len(front)) and (front[j+1] < self.book.length):
                page2 = self.book.pdfReader.pages[front[j + 1]]

            merged_page = self.merge_page_2(copy.copy(page1), copy.copy(page2))

            self.pdf_writer_front.add_page(merged_page)
            j += 2

    def special_back(self, back: []):
        j = 0
        page1 = PageObject.create_blank_page(None, self.book.width,
                                             self.book.height)
        page2 = PageObject.create_blank_page(None, self.book.width,
                                             self.book.height)

        while j < len(back):
            if back[j] < self.book.length:
                page1 = self.book.pdfReader.pages[back[j]]
            if (j + 1 < len(back)) and (back[j+1] < self.book.length):
                page2 = self.book.pdfReader.pages[back[j + 1]]

            merged_page = self.merge_page_2(copy.copy(page1), copy.copy(page2))

            self.pdf_writer_back.add_page(merged_page)
            j += 2

    def merge_page_2(self, page1: PageObject, page2: PageObject):
        width_to_height1 = float(self.book.height / (page1.mediabox.width * 2))
        height_to_width1 = float(self.book.width / page1.mediabox.height)

        width_to_height2 = float(self.book.height / (page2.mediabox.width * 2))
        height_to_width2 = float(self.book.width / page2.mediabox.height)

        cropleft1 = float(page1.cropbox.left)
        cropleft2 = float(page2.cropbox.left)
        cropbottom1 = float(page1.cropbox.bottom)
        cropbottom2 = float(page2.cropbox.bottom)

        transform1 = PyPDF2.Transformation() \
            .rotate(-90) \
            .scale(sx=height_to_width1,
                   sy=width_to_height1) \
            .translate(ty=self.book.height)

        transform2 = PyPDF2.Transformation() \
            .rotate(-90) \
            .translate(tx=0,
                       ty=0) \
            .scale(sx=height_to_width2,
                   sy=width_to_height2) \
            .translate(ty=self.book.height/2)

        full_view = RectangleObject((0, 0, 0, 0))
        full_view.lower_left = (0, 0)
        full_view.upper_right = (self.book.width, self.book.height)

        page1_viewable_area = RectangleObject((0, 0, 0, 0))
        page1_viewable_area.lower_left = (
                                          0,
                                          (self.book.height/2)
                                          # + cropleft1
                                         )
        page1_viewable_area.upper_right = (self.book.width, self.book.height)

        page2_viewable_area = RectangleObject((0, 0, 0, 0))
        page2_viewable_area.lower_left = (0, 0)
        page2_viewable_area.upper_right = (
                                           self.book.width,
                                           (self.book.height/2)
                                           # - (2 * cropleft2)
                                          )

        page1.add_transformation(transform1)
        page2.add_transformation(transform2)



        # page1.cropbox = page1_viewable_area
        page1.trimbox = page1_viewable_area
        # page1.mediabox = page1_viewable_area
        # page1.bleedbox = page1_viewable_area
        # page1.artbox = page1_viewable_area

        # page2.cropbox = page1_viewable_area
        page2.trimbox = page1_viewable_area     # words visible
        # page2.mediabox = page1_viewable_area
        # page2.bleedbox = page1_viewable_area
        # page2.artbox = page2_viewable_area

        page_base = PyPDF2.PageObject.create_blank_page(None,
                                                        width=self.book.width,
                                                        height=self.book.height)

        page_base.merge_page(page1, expand=True)
        # page_base.merge_page(page2, expand=True)

        return page_base

    def double_print(self):
        self.double_front()
        self.double_back()

    def double_front(self):
        list_copy = copy.deepcopy(self.pdf_writer_front)
        self.pdf_writer_front = PdfWriter()
        j = 0

        page2 = PageObject.create_blank_page(None, self.book.width,
                                             self.book.height)

        while j < len(list_copy.pages):
            page1 = list_copy.pages[j]
            if j + 1 <= len(list_copy.pages):
                page2 = list_copy.pages[j + 1]

            merged_page = self.merge_page_2(copy.copy(page1), copy.copy(page2))
            merged_page.rotate(180)

            self.pdf_writer_front.add_page(merged_page)
            j += 2

    def double_back(self):
        list_copy = copy.deepcopy(self.pdf_writer_back)
        self.pdf_writer_back = PdfWriter()
        j = 0

        page2 = PageObject.create_blank_page(None, self.book.width,
                                             self.book.height)

        while j < list_copy._get_num_pages():
            page1 = list_copy.pages[j]
            if j + 1 <= len(list_copy.pages):
                page2 = list_copy.pages[j + 1]

            merged_page = self.merge_page_2(copy.copy(page2), copy.copy(page1))
            merged_page.rotate(180)

            self.pdf_writer_back.add_page(merged_page)
            j += 2
