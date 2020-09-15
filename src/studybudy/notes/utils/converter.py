import sys
import os
from PyPDF2 import PdfFileReader
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
from io import StringIO


class Converter:
    def __init__(self):
        self.pages_text = []
        self.debug = 0
        # input option
        self.password = b''
        self.pagenos = set()
        self.maxpages = 0
        # output option
        self.outfile = None
        self.outtype = None
        self.imagewriter = None
        self.rotation = 0
        self.stripcontrol = False
        self.layoutmode = 'normal'
        self.encoding = 'utf-8'
        self.pageno = 1
        self.scale = 1
        self.caching = True
        self.showpageno = True
        self.laparams = LAParams()


    def pdf_to_html(self, file_path, output_file):
        self.opts = [('-o', output_file), ('-t', 'html')]
        self.args = [file_path]
        
        for (k, v) in self.opts:
            if k == '-d': self.debug += 1
            elif k == '-P': self.password = v.encode('ascii')
            elif k == '-o': self.outfile = v
            elif k == '-t': self.outtype = v
            elif k == '-O': self.imagewriter = ImageWriter(v)
            elif k == '-c': self.encoding = v
            elif k == '-s': self.scale = float(v)
            elif k == '-R': self.rotation = int(v)
            elif k == '-Y': self.layoutmode = v
            elif k == '-p': self.pagenos.update( int(x)-1 for x in v.split(',') )
            elif k == '-m': self.maxpages = int(v)
            elif k == '-S': self.stripcontrol = True
            elif k == '-C': self.caching = False
            elif k == '-n': self.laparams = None
            elif k == '-A': self.laparams.all_texts = True
            elif k == '-V': self.laparams.detect_vertical = True
            elif k == '-M': self.laparams.char_margin = float(v)
            elif k == '-W': self.laparams.word_margin = float(v)
            elif k == '-L': self.laparams.line_margin = float(v)
            elif k == '-F': self.laparams.boxes_flow = float(v)


        PDFDocument.debug = self.debug
        PDFParser.debug = self.debug
        CMapDB.debug = self.debug
        PDFPageInterpreter.debug = self.debug
        rsrcmgr = PDFResourceManager(caching=self.caching)

        if not self.outtype:
            self.outtype = 'text'
            if self.outfile:
                if self.outfile.endswith('.htm') or self.outfile.endswith('.html'):
                    self.outtype = 'html'
                elif self.outfile.endswith('.xml'):
                    self.outtype = 'xml'
                elif self.outfile.endswith('.tag'):
                    self.outtype = 'tag'
        if self.outfile:
            outfp = open(self.outfile, 'w', encoding=self.encoding)
        else:
            outfp = sys.stdout

       
        if self.outtype == 'text':
            device = TextConverter(rsrcmgr, outfp, laparams=self.laparams,
                                imagewriter=imagewriter)
        elif self.outtype == 'xml':
            device = XMLConverter(rsrcmgr, outfp, laparams=self.laparams,
                                imagewriter=self.imagewriter,
                                stripcontrol=self.stripcontrol)
        elif self.outtype == 'html':
            
            device = HTMLConverter(rsrcmgr, outfp, codec=self.encoding, scale=self.scale,
                                layoutmode=self.layoutmode, laparams=self.laparams,
                                imagewriter=self.imagewriter, debug=self.debug)
        elif self.outtype == 'tag':
            device = TagExtractor(rsrcmgr, outfp)
        else:
            return usage()
        for fname in self.args:
            with open(fname, 'rb') as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.get_pages(fp, self.pagenos,
                                            maxpages=self.maxpages, password=self.password,
                                            caching=self.caching, check_extractable=True):
                    page.rotate = (page.rotate+self.rotation) % 360
                    interpreter.process_page(page)
        device.close()
        outfp.close()
        return self.outfile


    def word_count(self,raw):
        text = raw
        word_count = 0
        for x in text:
            if x == " ":
                word_count += 1

        return word_count


    def get_pdf_text(self, file_path):
        base_name = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        name, ext = os.path.splitext(base_name)
        if ext != ".pdf":
            return False, "Only pdf Files Accepted"
        elif size <= 4000:
            return False, "File is empty"
        else:
            words = 0
            rsrcmgr = PDFResourceManager()
            sio = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, sio, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            with open(file_path, "rb") as fh:
                for page in PDFPage.get_pages(fh):
                    interpreter.process_page(page)

                content = sio.getvalue()
                word = self.word_count(content)
                words = words + word
                if words < 5:
                    return False, words, "Not Enough Words"
                else:
                    self.pages_text.append(content)
                    return True, words, self.pages_text
            # Cleanup
            # self.pages_text.append(content)
            device.close()
            sio.close()
            # return True, words, self.pages_text


    def count_questions(self, question_json):
        red = {
            "zinary"    : 0,
            "WH"        : 0,
            "gaps"      : 0,
            }
        total = len(question_json)
        for i in question_json:
            if i["question_type"] == "Binary Questions":
                red["zinary"] += 1
            elif i["question_type"] == "WH Questions":
                red["WH"] += 1
            elif i["question_type"] == "Fill in the Gap Questions":
                red["gaps"] += 1

        return total, red



    

   

