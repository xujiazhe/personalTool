# -*- coding: utf-8 -*-
#
# Created by xujiazhe on 2019-03-24.
#

import os
import re
import json

from PIL import Image, ImageChops

# from skimage import io

# from addBookFigures import bookDir

# os.chdir(bookDir)

lines = """figure-1.1.jpeg """

fnames = [fname for fname in lines.split('\n')]


def trimWhiteBorder(im):
	bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))

	diff = ImageChops.difference(im, bg)
	diff = ImageChops.add(diff, diff, 2.0, -100)
	bbox = diff.getbbox()
	if bbox:
		return im.crop(bbox)


def dealFigureBorder():
	# 书籍配图 切白边

	total = len(fnames)

	for cnt, fname in enumerate(fnames):
		im = Image.open(fname)
		cropped = trimWhiteBorder(im)
		cropped.save(fname.replace("figure", "deal", 1))
		print(cnt, fname)

	# im = Image.open('whatever.png')
	# .show()


def jsonOutlines():
	lines = open("olData").readlines()
	lines = filter(lambda x: x, (l.strip() for l in lines))
	lines = [l.replace('........', '_____', 1) for l in lines]
	olConfig = {}

	for l in lines:
		m = re.sub("(_\.+)", "", l)
		namePart, pageNum = m.split("____")

		chapterNo, title = namePart.split('\t')
		# title = title.decode('utf8')
		pageNum = int(pageNum)

		Title = "%s - %s" % (chapterNo, title)

		olConfig[Title] = pageNum + 15

	json.dump(olConfig, open("toc.json", "w"))

	# print >> open("toc.json", "w"), config
