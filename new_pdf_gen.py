from PyPDF2 import PdfReader, PdfWriter


class NewPDF:
    def __init__(self, pdf_name: str):
        pdf_document_name = pdf_name
        self.pdf = PdfReader(pdf_document_name)

        self.front_pdf = "front.pdf"
        self.back_pdf = "back.pdf"

        self.pdf_writer_front = PdfWriter()
        self.pdf_writer_back = PdfWriter()

        self.final_pdf = "final.pdf"
        self.final_pdf_writer = PdfWriter()

        self.num_pages = len(self.pdf.pages)
        #self.num_pages = self.pdf.getNumPages()

        self.pages_odd = False

        #self.combined()

    def set_pages_odd(self):
        if self.num_pages % 2 != 0:
            self.pages_odd = True
            self.num_pages += 1

    def divide_pages(self):
        # first divide pages in half
        # for front of pages for first half, take every even num
            # for second half of pages, take every odd num
        # for back of pages for first half, take every odd num
            # for second half of pages, take every even num
        #for page in range(self.pdf.getNumPages()):
        for page in range(len(self.pdf.pages)):
            current_page = self.pdf.pages[page]
            # first half of pages
            # since the page num is 1 behind, odd and even pages are opposite
            # 'page' in follow notes referes to real page numbers when the first number is 1
            if int(page) <= self.num_pages/2:
            #     # if page is odd, add to back pages
                if page % 2 == 0:
                    self.pdf_writer_front.add_page(current_page)
                # if page is even, add to front pages
                else:
                    self.pdf_writer_back.add_page(current_page)

            elif int(page) > self.num_pages/2:
                # if page is even, add to back pages
                if page % 2 == 0:
                    self.pdf_writer_back.add_page(current_page)
                # if page is odd, add to front pages
                else:
                    self.pdf_writer_front.add_page(current_page)

    def rearrange_pages(self):
        if len(self.pdf_writer_front.pages) == len(self.pdf_writer_back.pages):
            page = 0
            page_end = len(self.pdf_writer_front.pages)-1
            while page < len(self.pdf_writer_front.pages):
                current_page_front_left = self.pdf_writer_front.pages[page]
                current_page_back_left = self.pdf_writer_back.pages[page_end]
                page += 1
                page_end -= 1
                if page < len(self.pdf_writer_front.pages):
                    current_page_front_right = self.pdf_writer_front.pages[page_end]
                    current_page_back_right = self.pdf_writer_back.pages[page]
                    page += 1
                    page_end -= 1
                self.final_pdf_writer.add_page(current_page_front_left)
                if page < len(self.pdf_writer_front.pages):
                    self.final_pdf_writer.add_page(current_page_front_right)
                self.final_pdf_writer.add_page(current_page_back_left)
                if page < len(self.pdf_writer_front.pages):
                    self.final_pdf_writer.add_page(current_page_back_right)

                # if self.num_pages < len(self.final_pdf_writer.pages):
                #     self.final_pdf_writer.remove

                # if page < len(self.pdf_writer_front.pages):
                #     current_page_front_right = self.pdf_writer_front.pages[page]
                #
                #     self.final_pdf_writer.add_page(current_page_front_left)
                #     self.final_pdf_writer.add_page(current_page_front_right)
                #     self.final_pdf_writer.add_page(current_page_back_left)
                #     if (self.pages_odd and page < len(self.pdf_writer_front.pages)-1) or not self.pages_odd:
                #         current_page_back_right = self.pdf_writer_back.pages[page]
                #         self.final_pdf_writer.add_page(current_page_back_right)
                #     page += 1

        else:
            print("Front and back page count aren't the same")

        print("Front page count: ", len(self.pdf_writer_front.pages))
        print("Back page count: ", len(self.pdf_writer_back.pages))
        print("Total final page count: ", len(self.final_pdf_writer.pages))


    def save_to_disk(self):
            # Write the data to disk
            with open(self.final_pdf, "wb") as out:
                self.final_pdf_writer.write(out)
                print("created total", self.final_pdf)


    def combined(self):
        #self.set_pages_odd()
        self.divide_pages()
        self.rearrange_pages()
        self.save_to_disk()
