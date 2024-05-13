# -*- coding:utf-8 -*-
# @FileName : tag.py
# @Time : 2024/4/14 16:08
# @Author : fiv
from enum import Enum


class Tag(Enum):
    """
    Tag类定义部分记号对应的常量（内部表示）.
    """

    INT = "INT"
    REAL = "REAL"

    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"

    AND = "&&"
    OR = "||"

    EQEQ = "=="
    EQ = "="
    NE = "!="
    LE = "<="
    GE = ">="

    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    DOUBLESTAR = "**"
    SLASH = "/"
    DOUBLESLASH = "//"

    LPAR = "("
    RPAR = ")"
    LBRACE = "{"
    RBRACE = "}"
    LSQB = "["
    RSQB = "]"
    COMMA = ","
    SEMI = ";"
    DOT = "."
    COLON = ":"
    PERCENT = "%"
    COMMENT = "#"

    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"

    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"



if __name__ == "__main__":
    print(Tag.NUM)
