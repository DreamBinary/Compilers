# -*- coding:utf-8 -*-
# @FileName : tokenn.py
# @Time : 2024/4/14 16:37
# @Author : fiv
import numpy
from tag import Tag
from lexeme import Lexeme

class Token:
    """
    Token是描述所有记号的基类，它有一个数据成员tag以区分不同记号，构造函数赋tag值.
    """

    def __init__(self, tag: Tag):
        self.tag = tag


class Num(Token):
    """
    Num是描述整数的类，派生于Token，增加了一个数据成员value（词素，注意它的类型），它的构造函数在利用基类构造函数初始化tag值后，还给value赋了值。
    """

    def __init__(self, value: int):
        super().__init__(Tag("NUM"))
        self.value = value


class Word(Token):
    """
    Word描述保留字、标识符和各种复合运算符，派生于Token，增加了一个数据成员lexeme，它的构造函数有两个参数（前面是词素，后面是记号值）。7至13行定义一些Word类的常量。
    """
    def __init__(self, lexeme: str, tag: Tag):
        super().__init__(tag)
        self.lexeme = lexeme
