# -*- coding:utf-8 -*-
# @FileName : preprocess.py
# @Time : 2024/5/13 20:15
# @Author : fiv

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from work_one import Lexer, Tag
from grammar import EnumGrammar


class PreProcess:
    """
    预处理类, 先进行词法分析，然后处理成文法的形式，之后按文法处理
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.tokens = self.get_tokens()

    def get_tokens(self):
        lexer = Lexer(self.file_path)
        tokens, symtable, error = lexer.analyze()
        new_tokens = []
        for token, (r, c) in tokens:
            val, tag = token.lexeme, token.tag
            new_token = None
            if tag.value == EnumGrammar.IDENTIFIER.value:
                new_token = (val, EnumGrammar.IDENTIFIER)
            elif tag.value == Tag.KEYWORD.value:  # 关键字处理
                try:
                    new_token = EnumGrammar(val.upper())
                except ValueError:
                    print("No exist keyword: ", val)
            elif tag.value == Tag.INT.value:
                new_token = (val, EnumGrammar.INT)
            elif tag.value == Tag.REAL.value:
                new_token = (val, EnumGrammar.FLOAT)
            else:
                new_token = (val, EnumGrammar(tag.value))
            new_tokens.append(new_token)
        return new_tokens


if __name__ == '__main__':
    from ENV import PATH
    # TODO: 输出按文法转换之后的tokens
    path = PATH.DATA_PATH / "work2" / "miniRC.in2"
    s = PreProcess(path)
    for token in s.tokens:
        print(token)
