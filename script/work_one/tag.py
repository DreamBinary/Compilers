# -*- coding:utf-8 -*-
# @FileName : tag.py
# @Time : 2024/4/14 16:08
# @Author : fiv
from enum import Enum


class Tag(Enum):
    """
    Tag类定义部分记号对应的常量（内部表示）.
    """
    NUM = "NUM"
    INT = "INT"
    REAL = "REAL"

    ID = "ID"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"

    AND = "AND"
    OR = "OR"

    EQ = "EQ"
    NE = "NE"
    LE = "LE"
    GE = "GE"

    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"

    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    DOUBLESTAR = "DOUBLESTAR"
    SLASH = "SLASH"
    DOUBLESLASH = "DOUBLESLASH"

    LPAR = "LPAR"
    RPAR = "RPAR"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LSQB = "LSQB"
    RSQB = "RSQB"
    COMMA = "COMMA"
    SEMI = "SEMI"
    DOT = "DOT"
    COLON = "COLON"
    PERCENT = "PERCENT"

    ERROR = "ERROR"
    UNKNOW = "UNKNOW"



if __name__ == "__main__":
    print(Tag.NUM)
