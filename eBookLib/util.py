# -*- coding: utf-8 -*-
#
# Created by xujiazhe on 2019-04-19.
#

import hashlib

def fileMD5(FName):
    hash_md5 = hashlib.md5()
    try:
        f = open(FName, "rb")
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    except Exception, e:
        print "fname = ", FName
        print  e
        exit(3)

    return hash_md5.hexdigest()
