#! /usr/bin/env python3

# Test that key parts of Playbooks stayed in the right places

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
import sys


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
    return document, device, PDFPageInterpreter(rsrcmgr, device)


def load_playbook(playbook):
    document, device, interpreter = open_playbook(os.path.join("..", playbook) + ".pdf")

    pages = []
    # loop over all pages in the document
    for page in PDFPage.create_pages(document):

        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        pages.append(get_textboxes(layout._objs))

    return pages


PLAYBOOKS = ["cabalist",
             "hedge_mage",
             "inspired",
             "mentor",
             "pious",
             "primordial",
             "tech_adept",
             "voiced",
             "wayfarer"]    


LEFT_COLUMN, MIDDLE_COLUMN, RIGHT_COLUMN = range(3)


def near(num, target, rng=5):
    return abs(num - target) < rng


class TestPlaybooks(unittest.TestCase):

    def assert_box(self, textbox, text, page, column):
        if text not in self.found:
            self.found[text] = [False, page, column]
            
        if not textbox.get_text().startswith(text):
            return
        
        if column == LEFT_COLUMN:
            self.assertTrue(near(textbox.x0, 22))
        elif column == MIDDLE_COLUMN:
            self.assertTrue(near(textbox.x0, 397))
        elif column == RIGHT_COLUMN:
            self.assertTrue(near(textbox.x0, 709))
        else:
            self.assertTrue(False, "Column {} should have been one of LEFT_COLUMN, MIDDLE_COLUMN, or RIGHT_COLUMN".format(column))

        self.found[text][0] = True

    def setUp(self):
        self.found = {}
    
    def test_inspired(self):
        inspired = load_playbook("inspired")

        page = 1
        for textbox in inspired[page]:
            self.assert_box(textbox, "Name: ", page, LEFT_COLUMN)
            self.assert_box(textbox, "Starting Gear:", page, LEFT_COLUMN)

        for found in self.found:
            f = self.found[found]
            self.assertTrue(f[0], "'{}' was not found on expected page {} at column {}".format(found, f[1], f[2]))


if __name__ == "__main__":
    unittest.main()
