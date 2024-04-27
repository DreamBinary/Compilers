# -*- coding:utf-8 -*-
# @FileName : ui.py
# @Time : 2024/4/16 20:43
# @Author : fiv


import flet as ft
from lexer import Lexer


def process(file_path: str):
    lexer = Lexer(file_path)
    tokens, symtable = lexer.analyze()
    lexer.output()
    lexer.output_symtable()
    return tokens, symtable


def app(page: ft.Page):
    page.title = '词法分析器'

    # get file path

    # process

    # show result in table


if __name__ == '__main__':
    ft.app(target=app)
