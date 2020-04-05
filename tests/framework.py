#! /usr/bin/env python3

import unittest

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

import os

def get_textboxes(lt_objs):

    textboxes = []
    
    # loop over the object list
    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            textboxes.append(obj)
            #            textboxes.append({"x": obj.bbox[0], "y": obj.bbox[1],
#                              "text": obj.get_text()})
#            print("%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_')))

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            textboxes += get_textboxes(obj._objs)
    return textboxes


def open_playbook(playbook_file):
    # Open a PDF file.
    fp = open(playbook_file, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    return document, device, PDFPageInterpreter(rsrcmgr, device), fp


def load_playbook(playbook):
    document, device, interpreter, fp = open_playbook(os.path.join("..", playbook) + ".pdf")

    pages = []
    # loop over all pages in the document
    for page in PDFPage.create_pages(document):

        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        pages.append(get_textboxes(layout._objs))

    fp.close()
    return pages


COLUMN = {
    "LEFT": 22,
    "MIDDLE": 363,
    "RIGHT": 700
}

def get_text(textbox):
    return textbox.get_text().replace("\n", " ")


def near(num, target, rng=10):
    return abs(num - target) < rng


def identify_textbox(text, textbox):
    return "Text '{}' (x: {}, y: {})".format(text, textbox.x0, textbox.y0)


class TestPlaybooks(unittest.TestCase):

    def assert_box(self, page, page_num, text, col, cmp="startswith", x=None):
        found = False
        for textbox in page:
            if cmp == "startswith":
                if not get_text(textbox).startswith(text):
                    continue
            elif cmp == "contains":
                if text not in get_text(textbox):
                    continue
            found = True
            passed = False
            failing = None
            def assertion(x):
                if near(textbox.x0, x):
                    passed = True
                else:
                    failing = (identify_textbox(text, textbox)
                               + " not in column {} (near {})".format(col, COLUMN[col]))
            if x is None:
                assertion(COLUMN[col])
#                    raise ValueError("Column {} should have been one of LEFT_COLUMN, MIDDLE_COLUMN, or RIGHT_COLUMN".format(column))
            else:
                assertion(x)
            if passed:
                self.assertTrue(False, failing)
        self.assertTrue(found, "Text '{}' should have been found on page {} in column {}".format(
            text, page_num, col))

    def playbook_test(self, playbook_file, name, skip_paradigm=False):
        playbook = load_playbook(playbook_file)

        page_num = 0
        page = playbook[page_num]
        if not skip_paradigm:
            self.assert_box(page, page_num, "Paradigm List", "LEFT")
        self.assert_box(page, page_num, name, "MIDDLE", x=446)
        self.assert_box(page, page_num, name, "RIGHT")

        page_num = 1
        page = playbook[page_num]
        self.assert_box(page, page_num, "Name: ", "LEFT")
        self.assert_box(page, page_num, "Starting Gear:", "LEFT", "contains")
        self.assert_box(page, page_num, "Health", "MIDDLE", x=521)
        self.assert_box(page, page_num, "Get an Advanced", "MIDDLE", "contains")
        self.assert_box(page, page_num, name + "'s Moves", "RIGHT")
        self.assert_box(page, page_num, "exchange a moment of humanity", "RIGHT", "contains")
        return playbook
