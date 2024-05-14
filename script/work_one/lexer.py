# -*- coding:utf-8 -*-
# @FileName : lexer.py
# @Time : 2024/4/14 16:02
# @Author : fiv

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), os.pardir)))

from pathlib import Path
from tag import Tag
from tokenn import Word


class Lexer:
    """
    Lexer是完成词法分析功能的类，数据成员line为行号，peek是向前的一个字符，words是符号表。成员函数reserve将给定记号加入符号表。它的构造函数(8至17行)将所有保留字加入符号表。
    """

    def __init__(self, in_path: Path):
        self.in_path = in_path
        self.words = {}
        self.init_words()
        self.text = open(in_path, 'r').read()

        self.index = 0
        self.max = len(self.text)
        self.line = 1
        self.column = 0
        self.peek = ' '
        self.tokens = []  # [(Word, (line, column))]
        self.error = []  # (line -> int, column -> int, msg -> str)
        self.symtable = {}  # {tag -> {lexeme}}
        self.end_flag = "@$__$$**END@__++fiv"

    def analyze(self):
        while self.peek != self.end_flag:
            w = self.scan()
            if w is not None:
                self.tokens.append((w, (self.line, self.column - len(w.lexeme))))
        return self.tokens, self.symtable, self.error
        # self.check_error()

    def init_words(self):
        words = [
            "if", "else", "while", "return", "do", "break", "continue", "until", "for", "switch", "case", "default",
            "integer", "double", "bool", "char", "string",
            "true", "false", "void", "function", "main",
            "print", "read", "write", "readln", "writeln", "scanf", "printf",
        ]
        for i, w in enumerate(words):
            self.reserve(Word(w, Tag.KEYWORD))

    def reserve(self, w: Word):
        self.words[w.lexeme] = w

    def add2symtable(self, w: Word):
        lexeme, tag = w.lexeme, w.tag.value
        if tag not in self.symtable:
            self.symtable[tag] = {lexeme}
        else:
            self.symtable[tag].add(lexeme)

    def readch(self):
        if self.index >= self.max:  # 文件结束
            self.peek = self.end_flag  # 标志文件结束
            self.column += 1
            return
        self.peek = self.text[self.index]
        self.index += 1  # 读取下一个字符
        self.column += 1  # 更新列号  行号由\n更新
        # print(self.line, self.column, self.peek)

    def check_readch(self, c):
        self.readch()
        if self.peek != c:
            return False
        self.peek = ' '
        return True

    def scan_number(self) -> str:
        x = 0.0
        while True:
            x = x * 10 + int(self.peek)
            self.readch()
            if not self.peek.isdigit():
                break
        if self.peek != '.':
            return str(int(x))
        self.readch()
        d = 10
        while True:
            x += int(self.peek) / d
            d *= 10
            self.readch()
            if not self.peek.isdigit():
                break
        return str(x)

    # def scan_bracket(self):
    #     if self.peek == '(':
    #         self.stack.append(('(', (self.line, self.column - 1)))
    #         self.readch()
    #         return Word('(', Tag.LPAR)
    #     elif self.peek == '{':
    #         self.stack.append(('{', (self.line, self.column - 1)))
    #         self.readch()
    #         return Word("{", Tag.LBRACE)
    #     elif self.peek == '[':
    #         self.stack.append(('[', (self.line, self.column - 1)))
    #         self.readch()
    #         return Word("[", Tag.LSQB)
    #     else:
    #         try:
    #             if self.peek == ')' and self.stack[-1][0] == '(':
    #                 self.stack.pop()
    #                 self.readch()
    #                 return Word(")", Tag.RPAR)
    #             elif self.peek == '}' and self.stack[-1][0] == '{':
    #                 self.stack.pop()
    #                 self.readch()
    #                 return Word("}", Tag.RBRACE)
    #             elif self.peek == ']' and self.stack[-1][0] == '[':
    #                 self.stack.pop()
    #                 self.readch()
    #                 return Word("]", Tag.RSQB)
    #             else:
    #                 peek = self.peek
    #                 self.readch()
    #                 self.error(self.line, self.column, f"unexpected symbol {peek}")
    #                 return Word(peek, Tag.ERROR)
    #         except IndexError:
    #             peek = self.peek
    #             self.readch()
    #             self.error(self.line, self.column, f"unexpected symbol {peek}")
    #             return Word(peek, Tag.ERROR)

    def scan_bracket(self):
        if self.peek == '(':
            self.readch()
            return Word('(', Tag.LPAR)
        elif self.peek == ')':
            self.readch()
            return Word(")", Tag.RPAR)
        elif self.peek == '{':
            self.readch()
            return Word("{", Tag.LBRACE)
        elif self.peek == '}':
            self.readch()
            return Word("}", Tag.RBRACE)
        elif self.peek == '[':
            self.readch()
            return Word("[", Tag.LSQB)
        elif self.peek == ']':
            self.readch()
            return Word("]", Tag.RSQB)

    def scan(self):
        while True:
            if self.peek == ' ' or self.peek == '\t':
                self.readch()
            elif self.peek == '\n':
                self.line += 1
                self.column = 0
                self.readch()
            else:
                break
        # symbols
        if self.peek == '&':
            if self.check_readch('&'):
                return Word("&&", Tag.AND)
            else:
                return Word("&", Tag.AND)
        elif self.peek == '|':
            if self.check_readch('|'):
                return Word("||", Tag.OR)
            else:
                return Word("|", Tag.OR)
        elif self.peek == '=':
            if self.check_readch('='):
                return Word("==", Tag.EQEQ)
            else:
                return Word("=", Tag.EQ)
        elif self.peek == '!':
            if self.check_readch('='):
                return Word("!=", Tag.NE)
            else:
                return Word("!", Tag.NE)
        elif self.peek == '<':
            if self.check_readch('='):
                return Word("<=", Tag.LE)
            else:
                return Word("<", Tag.LE)
        elif self.peek == '>':
            if self.check_readch('='):
                return Word(">=", Tag.GE)
            else:
                return Word(">", Tag.GE)
        elif self.peek == '+':
            self.readch()
            return Word("+", Tag.PLUS)
        elif self.peek == '-':
            self.readch()
            return Word("-", Tag.MINUS)
        elif self.peek == '*':
            if self.check_readch('*'):
                return Word("**", Tag.DOUBLESTAR)
            else:
                return Word("*", Tag.STAR)
        elif self.peek == '/':
            if self.check_readch('/'):
                return Word("//", Tag.DOUBLESLASH)
            else:
                return Word("/", Tag.SLASH)
        elif self.peek == ',':
            self.readch()
            return Word(",", Tag.COMMA)
        elif self.peek == ';':
            self.readch()
            return Word(";", Tag.SEMI)
        elif self.peek == ':':
            self.readch()
            return Word(":", Tag.COLON)
        elif self.peek == '%':
            self.readch()
            return Word("%", Tag.PERCENT)
        elif self.peek == '#':  # comment
            t = ""
            while self.peek != '\n':
                t += self.peek
                self.readch()
            return Word(t, Tag.COMMENT)
        elif self.peek == '.':
            self.readch()
            if self.peek.isdigit():
                num = self.scan_number()
                return Word("." + str(num), Tag.REAL)
        elif self.peek == '(' or self.peek == ')' or self.peek == '[' or self.peek == ']' or self.peek == '{' or self.peek == '}':
            return self.scan_bracket()

        # digits
        b = ""
        if self.peek.isdigit():
            num = self.scan_number()

            if self.peek.isalpha():  # 检测数字后面是否跟字母, 数字和字母可以组成标识符。而不是将数字和字母分开
                b += str(num)
            else:
                if '.' in num:
                    return Word(num, Tag.REAL)
                else:
                    return Word(num, Tag.INT)

        # words
        if self.peek.isalpha() or self.peek == '_':
            while True:
                b += self.peek
                self.readch()
                if not self.peek.isalnum() and self.peek != '_':
                    break
            if b == self.end_flag:
                return None
            w = self.words.get(b)
            if w is not None:
                self.add2symtable(w)
                return w
            if not b.isidentifier():  # 检测是否是合法的标识符
                w = Word(b, Tag.ERROR)
                self.error.append((self.line, self.column - len(b), f"invalid identifier {b}"))
            else:
                w = Word(b, Tag.IDENTIFIER)
                self.add2symtable(w)
            return w

        # unknown
        if self.peek != self.end_flag:  # end_flag 标志着文件结束
            w = Word(self.peek, Tag.ERROR)
            self.error.append((self.line, self.column, f"unknown symbol {self.peek}"))
            self.readch()
            return w

    # def check_error(self):
    #     if self.stack:
    #         for s, (r, c) in self.stack:
    #             self.error(r, c, f"unmatched bracket {s}")
    #     print("Lexical analysis completed")

    def output(self):
        with open(PATH.OUTPUT_PATH / str(self.in_path.stem + ".out"), "w") as f:
            print("{:<10} | {:<15} | {:<10} | {:<10}".format("lexeme", "tag", "row", "column"))
            f.write("{:<10} | {:<15} | {:<10} | {:<10}\n".format("lexeme", "tag", "row", "column"))
            print("-" * 50)
            f.write("-" * 50 + "\n")
            for token, (r, c) in self.tokens:
                print("{:<10} | {:<15} | {:<10} | {:<10}".format(token.lexeme, token.tag.value, r, c))
                f.write("{:<10} | {:<15} | {:<10} | {:<10}\n".format(token.lexeme, token.tag.value, r, c))
            print("\n" + "-" * 50)
            f.write("\n" + "-" * 50 + "\n")
            if self.error:
                print("Error:")
                f.write("Error:\n")
                for r, c, msg in self.error:
                    print(f"line {r}, column {c}: {msg}")
                    f.write(f"line {r}, column {c}: {msg}\n")

    def output_symtable(self):
        with open(PATH.OUTPUT_PATH / str(self.in_path.stem + ".sym"), "w") as f:
            print("{:<15} | {:<15}".format("lexeme", "tag"))
            f.write("{:<15} | {:<15}\n".format("lexeme", "tag"))
            print("-" * 30)
            f.write("-" * 30 + "\n")
            for tag, lexemes in self.symtable.items():
                lexemes = sorted(lexemes)
                for lexeme in lexemes:
                    print("{:<15} | {:<15}".format(tag, lexeme))
                    f.write("{:<15} | {:<15}\n".format(tag, lexeme))

    def output_error(self):
        if self.error:
            with open(PATH.OUTPUT_PATH / str(self.in_path.stem + ".err"), "w") as f:
                print("Error:")
                f.write("Error:\n")
                for r, c, msg in self.error:
                    print(f"line {r}, column {c}: {msg}")
                    f.write(f"line {r}, column {c}: {msg}\n")


if __name__ == '__main__':
    from ENV import PATH

    in_path = PATH.DATA_PATH / "work1" / "miniRC.in"
    lexer = Lexer(in_path)
    lexer.analyze()
    lexer.output()
    lexer.output_symtable()
    lexer.output_error()

"""
Example Input:
miniRC=function(integer N, integer K, double rc){
     integer a[10][20];
     double b[19];

     if(N==1) return(0);
     integer KL=floor(K * rc);         #split N 
     if(KL < 1 || KL > (K-1))
            KL = 1;
     else if (KL > .5*K)
            KL = ceiling(KL / 2.0)

     KR = K - KL

     integer NL = ceiling(N * KL / K)      #split N
     integer NR = N - NL

     return( 1+(NL * miniRC(NL, KL, rc) + NR * miniRC(NR, KR, rc)) / N)
}

Example Output:
<id, miniRC>
<=>
<function>
<(>
<integer>
 <id, N>
<,> 
<integer>
<id, K>
<,> 
<double> 
<id, rc>
<)>
<{>
<integer> 
<id, a>
<[>
<INT, 10>
<]>
<[>
<INT, 20>
<]>
<;>
 <double>
<id, b>
<[>
<INT, 19>
<]>
<;>
 <if>
<(>
<id, N>
<==>
<INT, 1>
<)>
 <return>
<(>
<NUM, 0>
<)>
<;>
 <integer> 
<id, KL>
<=>
<id, floor>
<(>
<id, K>
 <*>
<id, rc>
<)>
<;>   
 <if>
<(>
<id, KL> 
<<>
<INT, 1>
<||>
<id, KL>
<>>
<(>
<id, K>
<->
<INT, 1>
<)>
<)>
 <id, KL> 
<=>
<INT, 1>
<;>
 <else> 
<if> 
<(>
<id, KL>
 <>>
<REAL, 0.5>
<*>
<id,K>
<)>
 <id, KL>
 <=> 
<id, ceiling>
<(>
<id, KL>
</>
<REAL, 2.0>
<)>
<id, KR>
<=>
<id, K>
<->
<id, KL>
<integer>
<id, NL>
<=>
<id, ceiling>
<(>
<id, N>
<*> 
<id, KL>
</>
<id, K>
<)>  
<integer>
<id, NR>
<=>
<id, N>
<->
<id, NL>
<return>
<(>
<INT, 1>
<+>
<(>
<id, NL>
<*>
<id, miniRC>
<(>
<id, NL>
<,>
<id, KL>
<,>
<id, rc>
<)>
<+>
<id, NR>
<*>
<id, miniRC>
<(>
<id, NR>
<,>
<id, KR>
<,>
<id, rc>
<)>
<)>
</>
<id, N>
<)>     
<}>
"""
