# -*- coding: utf-8 -*-
#
# Created by xujiazhe on 2019-03-24.
#

import sys
import os
import re
import collections


from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt

from addBookFigures import bookDir, bookName


# converts pdf, returns its text content as a string 
def convert(fname, pages=None):
    if not pages:
        pagenums = list()
    else:
        pagenums = list(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


os.chdir(bookDir)
# 提取目录部分的文本
outLines = convert(bookName, range(16))
print >> open("olData", "w"), outLines

lines = """figure-1.1.pdf
figure-12.13.pdf
figure-14.3.pdf
figure-16.2.pdf"""


"""
pattern = "^figure-(\d+\.\d+)\.pdf$"
ls = lines.split()

dd = {re.match(pattern, l).group(1): l for l in ls}
kd = collections.OrderedDict(sorted(dd.items(), key=lambda t: map(int, t[0].split('.'))))

print len(kd)
"""
