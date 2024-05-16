# -*- coding:utf-8 -*-
# @FileName : grammar.py
# @Time : 2024/5/12 21:00
# @Author : fiv


from enum import Enum
import re


class EnumGrammar(Enum):
    def __hash__(self):
        return super().__hash__()

    PROGRAM_ = 'PROGRAM_'
    PROGRAM = 'PROGRAM'
    FUN = 'FUN'  # 文法中
    VARIABLE = 'VARIABLE'
    FUNCTION = 'FUNCTION'  # Keyword
    STATEMENT = 'STATEMENT'
    EXPRESSION = 'EXPRESSION'
    TYPE = 'TYPE'
    # DIGIT = 'DIGIT'
    INTEGER = 'INTEGER'
    INT = 'INT'
    DOUBLE = 'DOUBLE'
    FLOAT = 'FLOAT'
    # LETTER = 'LETTER'
    IDENTIFIER = 'IDENTIFIER'
    IF = 'IF'
    ELSE = 'ELSE'
    REPEAT = 'REPEAT'
    UNTIL = 'UNTIL'
    FOR = 'FOR'
    BREAK = 'BREAK'
    RETURN = 'RETURN'
    EPSILON = 'EPSILON'
    STATEMENTLIST = 'STATEMENTLIST'
    EXPRESSIONLIST = 'EXPRESSIONLIST'

    EQ = '='
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    SLASH = '/'
    LT = '<'
    GT = '>'
    LE = '<='
    GE = '>='
    EQEQ = '=='
    NE = '!='
    AND = '&&'
    OR = '||'
    INC = '++'
    DEC = '--'
    LPAR = '('
    RPAR = ')'
    LBRACE = '{'
    RBRACE = '}'
    LSQB = '['
    RSQB = ']'
    COMMA = ','
    SEMI = ';'
    DOT = '.'
    COMMENT = '#'


# class EnumSymbol(Enum):
#     def __hash__(self):
#         return super().__hash__()

class Grammar:
    def __init__(self, grammar_file: str):
        self.grammar = open(grammar_file, 'r').read()
        self.grammar_dict = self.covert_grammar()
        self.all_symbols = self.get_all_symbols()

    def get_all_symbols(self):
        sym = []
        rm = ["digit", "int", "float", "letter", "identifier", "comment"]  # 使用词法分析器处理
        # add EnumGrammar
        for k in EnumGrammar:
            if k.name not in rm:
                sym.append(k)
        # add EnumSymbol
        # for k in EnumSymbol:
        #     sym.append(k)
        # sym = sorted(sym, key=lambda x: x.name)
        return sym

    def covert_grammar(self):
        rm = ["digit", "int", "float", "letter", "identifier", "comment"]  # 使用词法分析器处理
        # covert grammar to dict, str
        tmp_grammar_dict = {}
        for line in self.grammar.split('\n'):
            if not line:
                continue
            key, value = line.split('->')
            key = key.strip()
            if key in rm:
                continue
            value = value.strip()
            # split by '|' not ' ||'
            value = value.split(" | ")  # 注意空格
            tmp_grammar_dict[key] = value

        # convert grammar_dict to EnumGrammar and EnumSymbol
        # new_grammar_dict = {}
        new_grammar_dict = []  # 改增广文法
        for key, value in tmp_grammar_dict.items():
            # convert key to EnumGrammar
            new_key = getattr(EnumGrammar, key.upper())
            new_value = []
            for v in value:
                # convert value to EnumGrammar
                nv = []
                for vv in v.split(' '):
                    if vv:
                        if not vv.isalnum():
                            # convert value to EnumSymbol, = -->> EQ
                            nv.append(EnumGrammar(vv))
                        elif len(vv) == 1:
                            nv.append(str(vv))
                        else:
                            # convert value to EnumGrammar
                            nv.append(EnumGrammar(vv.upper()))
                new_value.append(tuple(nv))
            for tv in new_value:
                new_grammar_dict.append((new_key, tv))
        new_grammar_dict.insert(0, (EnumGrammar.PROGRAM_, (new_grammar_dict[0][0],)))
        return new_grammar_dict

    def get_grammar(self):
        return self.grammar_dict, self.all_symbols


if __name__ == '__main__':
    import os

    dirr = os.path.dirname(__file__)
    grammar = os.path.join(dirr, 'grammar.txt')
    g = Grammar(grammar)
    grammar_dict, sym = g.get_grammar()

    # TODO: print grammar_dict
    # for k, v in grammar_dict.items():
    #     print(k, " -> ", end='')
    #     for vv in v:
    #         print(vv, end=' | ')
    #         # print(tuple([(vvv.value if type(vvv) is not str else vvv) for vvv in vv]), end=' | ')
    #     print()
    for i in grammar_dict:
        print(i)

    for i in sym:
        print(i)
