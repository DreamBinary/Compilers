# -*- coding:utf-8 -*-
# @FileName : sdt.py
# @Time : 2024/5/18 19:54
# @Author : fiv

from script.slr import SLR


class SDT:
    """
    语法制导翻译 SLR(1) -> SDT
    """
    def __init__(self, input_file):
        self.slr = SLR(input_file)


    def parse(self):
        pass

