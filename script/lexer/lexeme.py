# -*- coding:utf-8 -*-
# @FileName : lexeme.py
# @Time : 2024/4/15 16:55
# @Author : fiv

from tag import Tag


class Lexeme:
    """
    Lexeme是描述词素的类，它的构造函数有两个参数（前面是词素，后面是记号值）。
    """

    def __init__(self, lexeme: str, tag: Tag):
        self.lexeme = lexeme
        self.tag = tag
