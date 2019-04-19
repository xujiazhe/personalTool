# coding: utf-8

# 合并两个电子书库 根据md5去重
#    单个去重
#    从副库提出来要加入的

import os
import os.path as path
from os.path import join as join

import pandas as pd

from util import fileMD5

home = path.expanduser('~')
baiduLib = join(home, "百度云同步盘/图书馆")
icloudOld = join(home, "iCloud 云盘（归档）/图书馆")
icloudCur = join(home, "books/图书馆")


# 工作目录切换
def wd(fn):
    def func2(*args, **kwargs):
        pre_wd = os.getcwd()
        result = fn(*args, **kwargs)
        os.chdir(pre_wd)
        return result

    return func2


# 获取书库的 概况  (md5, 名字, 全名)
@wd
def libOverview(eBookLibraryPath):
    os.chdir(eBookLibraryPath)
    result = []

    for csdir, dirs, files in os.walk('.'):
        for fname in files:
            if fname.startswith('.'):
                continue

            fileName = join(csdir, fname)
            md = fileMD5(fileName)

            result.append(
                (md, fname, fileName)
            )

    return result


if __name__ == '__main__':
    bd = libOverview(baiduLib)
    io = libOverview(icloudOld)
    il = libOverview(icloudCur)

    bd_df = pd.DataFrame(bd, columns=["md5", "书名", "路径名"])
    io_df = pd.DataFrame(io, columns=["md5", "书名", "路径名"])
    ic_df = pd.DataFrame(il, columns=["md5", "书名", "路径名"])

    # 单个书库查重
    bd_dupl = bd_df.groupby(['md5']).filter(lambda x: x.md5.count() > 1)
    io_dupl = io_df.groupby(['md5']).filter(lambda x: x.md5.count() > 1)
    ic_dupl = ic_df.groupby(['md5']).filter(lambda x: x.md5.count() > 1)

    # 合并前 差异检查
    bd_additional = bd_df[bd_df.md5.isin(set(bd_df.md5) - set(ic_df.md5))]  # 百度旧库 不在新库中的书
    io_additional = io_df[io_df.md5.isin(set(io_df.md5) - set(ic_df.md5))]  # 老库不在新库中的书
