# -*- coding: utf-8 -*-

# 备份照片去重

import os
from os.path import join as join

from util import fileMD5

imagePath = u"~/Downloads/本机照片/"


def md2fname(wdir):
    local_books = {}
    os.chdir(wdir)
    for cspath, dirs, files in os.walk('.'):

        if len(dirs) and dirs[-1].startswith('.'):
            continue

        for fname in files:
            if fname.startswith('.'):
                continue
            fileName = join(cspath, fname)
            md = fileMD5(fileName)
            if md in local_books:
                print cspath, fname
                continue
            local_books[md] = [cspath, fname]

    return local_books


Dict = md2fname(imagePath)

# with open('mdfiles.data', 'wb') as f:
#    pickle.dump(local_books, f)
