# -*- coding:utf-8 -*-
# @FileName : semantic_analyzer.py
# @Time : 2024/4/4 14:52
# @Author : fiv


# 语义分析器
class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.error = False
        self.error_msg = ""
        self.result = []

    def analyze(self):
        self.program()
        return self.result

    def program(self):
        self.statement_list()
        self.match("EOF")