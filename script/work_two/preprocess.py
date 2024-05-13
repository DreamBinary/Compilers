# -*- coding:utf-8 -*-
# @FileName : preprocess.py
# @Time : 2024/5/13 20:15
# @Author : fiv

from script.work_one import Lexer
from ENV import PATH
from script.work_one import Tag
from grammar import EnumGrammar, EnumSymbol


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
            if tag.value == EnumGrammar.IDENTIFIER.value:
                new_token = (val, EnumGrammar.IDENTIFIER)
            elif tag.value == Tag.KEYWORD.value:
                if val == "if":
                    new_token = (val, EnumGrammar.IF)
                elif val == "else":
                    new_token = (val, EnumGrammar.ELSE)
                elif val == "integer":
                    new_token = (val, EnumGrammar.INTEGER)
                elif val == "double":
                    new_token = (val, EnumGrammar.DOUBLE)
                elif val == "return":
                    new_token = (val, EnumGrammar.RETURN)
                elif val == "function":
                    new_token = (val, EnumGrammar.FUNCTION)
                elif val == "until":
                    new_token = (val, EnumGrammar.UNTIL)
                elif val == "repeat":
                    new_token = (val, EnumGrammar.REPEAT)
                elif val == "break":
                    new_token = (val, EnumGrammar.BREAK)
                elif val == "for":
                    new_token = (val, EnumGrammar.FOR)
                else:
                    print("ERROR:", print(val, tag))
            elif tag.value == Tag.INT.value:
                new_token = (val, EnumGrammar.INT)
            elif tag.value == Tag.REAL.value:
                new_token = (val, EnumGrammar.FLOAT)
            else:
                new_token = (val, EnumSymbol(tag.value))
            new_tokens.append(new_token)
        return new_tokens


if __name__ == '__main__':
    # TODO: 输出按文法转换之后的tokens
    path = PATH.DATA_PATH / "work2" / "miniRC.in2"
    s = PreProcess(path)
    for token in s.tokens:
        print(token)
