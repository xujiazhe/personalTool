# -*- coding: utf-8 -*-
#
# Created by xujiazhe on 2019-03-24.
#
# 添加图片
# 1, 匹配提取 配图信息(页号, 位置)
#    验证数目 与 重复情况
# 2, 裁剪 图片 边白
# 3, 在 每个配图位置上插入图片, 生成效果的pdf
# 添加目录
#    目录编辑复制
#    截图转换
#      python处理


import os
import re
from StringIO import StringIO

import PyPDF2 as pypdf
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from reportlab.pdfgen import canvas

bookDir = "~/Downloads/Internetworking with TCPIP"
bookName = "用TCP.IP进行网际互联-V1第5版中文.pdf"
figurePath = "Internetworking with TCPIP(TCPIP网络互连)卷I(第5版)插图-Comer/deal-%s.jpeg"

os.chdir(bookDir)
bookFp = open(bookName, 'rb')
pdfBook = pypdf.PdfFileReader(open(bookName, "rb"))
figurePosPattern = re.compile("^\xe5\x9b\xbe (\d+\.\d+) {2}")  # 图 1.1  网络拓扑结构图

figureInfoGroupsByPage = {}

parser = PDFParser(bookFp)
# 创建一个PDF文档对象存储文档结构
document = PDFDocument(parser)
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
# 创建一个PDF资源管理器对象来存储共赏资源
rsrcmgr = PDFResourceManager()
# 设定参数进行分析
laparams = LAParams()
# 创建一个PDF设备对象
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
# 创建一个PDF解释器对象
interpreter = PDFPageInterpreter(rsrcmgr, device)

for pIndex, page in enumerate(PDFPage.create_pages(document)):
    interpreter.process_page(page)  # 接受该页面的LTPage对象
    layout = device.get_result()  # return text image line curve

    for x in layout:
        if not isinstance(x, LTTextBoxHorizontal): continue
        figureName = x.get_text()[:15].encode("utf-8")
        if not figureName: continue
        m = figurePosPattern.match(figureName)
        if not m: continue

        FID = m.group(1)
        width, height = Image.open(figurePath % FID).size

        figureInfoGroupsByPage.setdefault(pIndex, [])
        figureInfoGroupsByPage[pIndex].append((FID, x.bbox, (width, height)))

bookFp.close()

# 保存中间结果
print figureInfoGroupsByPage

# 校验
# oa 两个空格原序  ob一个空格原序
# aab = [e for e in a if e[1] in set(e[1] for e in ab)]
# aab.sort(key=lambda x: x[1])

# aab = [e for e in a if e[1] in set(e[1] for e in ab)]
# abb = [e for e in b if e[1] in set(e[1] for e in ab)]

# aab_order = [e for e in oa if e[1] in set(e[1] for e in ab)]
# abb_order = [e for e in ob if e[1] in set(e[1] for e in ab)]
# 多一个图片 32.1
# 匹配空格就匹配两个的 验续abb_order靠谱
# 12.12 错页面


specialFidList = ['7.3', '8.10', '9.4', '9.7', '9.12', '9.15', '12.12', '12.15']

pdfWriter = PdfFileWriter()

for pix in sorted(figureInfoGroupsByPage.keys()):
    fgInfoOfCurPage = figureInfoGroupsByPage[pix]
    removeList = [e for e in fgInfoOfCurPage if e[0] in specialFidList]
    if len(removeList) == 0: continue

    if len(removeList) == len(figureInfoGroupsByPage[pix]):
        del figureInfoGroupsByPage[pix]
    else:
        figureInfoGroupsByPage[pix] = [e for e in fgInfoOfCurPage if e[0] not in specialFidList]

    figureInfoGroupsByPage.setdefault(pix - 1, [])
    figureInfoGroupsByPage[pix - 1].extend(removeList)

# pos  73.68019000000021, 514.16014, 522.0001800000002, 526.14382 x0, y0, x1, y1

for pix in range(pdfBook.getNumPages()):
    curPage = pdfBook.getPage(pix)

    if pix not in figureInfoGroupsByPage:
        pdfWriter.addPage(curPage)
        continue

    fgInfoOfCurPage = figureInfoGroupsByPage[pix]
    figureBg = None
    for i, (figureId, pos, fSize) in enumerate(fgInfoOfCurPage):
        # 位置居中 缩小二倍   595 pdf页宽
        fw, fh = fSize[0] / 2, fSize[1] / 2
        sx, sy = (595 - fw) / 2, pos[-1] + 2

        if figureId in specialFidList: sy = 82  # 如果图在上页, 就画到上页的结尾

        imgTemp = StringIO()
        imgDoc = canvas.Canvas(imgTemp)
        imgDoc.drawImage(figurePath % figureId, sx, sy, fw, fh)  # 根据位置start_position with size 160x160
        imgDoc.save()

        if i:
            otherFigureBg = PdfFileReader(StringIO(imgTemp.getvalue())).getPage(0)
            figureBg.mergePage(otherFigureBg)
        else:
            figureBg = PdfFileReader(StringIO(imgTemp.getvalue())).getPage(0)
    figureBg.mergePage(curPage)

    pdfWriter.addPage(figureBg)

figureBookName = os.path.join(r'figureBook.pdf')
with open(figureBookName, "wb") as fp:
    pdfWriter.write(fp)
