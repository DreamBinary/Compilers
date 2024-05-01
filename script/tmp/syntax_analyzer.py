# -*- coding:utf-8 -*-
# @FileName : syntax_analyzer.py
# @Time : 2024/4/4 14:52
# @Author : fiv


# 语法分析器
# LR(1)语法分析器

class SyntaxAnalyzer:
    def __init__(self):
        self.idx = 0
        self.codes = []
        self.NXQ = 1
        # 定义符号表
        self.const_attri_sheet = []
        self.variable_attri_sheet = []
        self.func_attr_sheet = []
        self.temp_attri_sheet = []
        self.quad_codes = []
        self.quad_code = {}
        self.quad_code['op'] = ''

    def doentry(self, token: list):
        '''
        翻译入口
        :param token:
        :return:
        '''
        self.codes = token
        self.program()
        print('语法分析完成')

    def program(self):
        pass
