import sys
import os
from tkinter import W
import fitz
import cv2
import numpy as np
import yaml

from pdfcropper.utils.error import ErrorHandler

class PDF_to_PNG:
    def __init__(self, pdf_file, png_files, dpi=300, log='ignore',
    same_root=True, error='all'):
        self.log = log
        self.dpi = dpi
        self.zoom = self.dpi / 72  # zoom factor, standard dpi is 72
        self.pdf_file_fullpath = pdf_file
        self.path, self.pdf_file = os.path.split(pdf_file)
        self.png_files = png_files
        self.error_handler = ErrorHandler(error=error)

        self.load_pdf()
        self.convert_pdf_pages_to_png()
        

    
    def load_pdf(self):
        if self.log == 'all':
            print(f'Loading {self.pdf_file}')
        self.pdf_pages = fitz.open(self.pdf_file_fullpath)
        self.pdf_page_number = len(self.pdf_pages)

        if self.pdf_page_number != len(self.png_files):
            msg = f'Number of pages in pdf file ' +\
                f'{self.pdf_file_fullpath}:{self.pdf_page_number} ' +\
                f'does not match output number {len(self.png_files)}.'
            self.error_handler.send(IndexError, msg)


    def convert_pdf_pages_to_png(self):
        magnify = fitz.Matrix(self.zoom, self.zoom)  # takes care of zooming
        for i, image in enumerate(self.pdf_pages):
            if self.log == 'all':
                print(f'Convert {self.pdf_file}:{i} to {self.png_files[i]}.')
            pix = image.get_pixmap(matrix=magnify)
            pix.set_dpi(self.dpi, self.dpi)
            pix.save(os.path.join(self.path, self.png_files[i]))
