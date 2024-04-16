# -*- coding:utf-8 -*-
# @FileName : lexer.py
# @Time : 2024/4/14 16:02
# @Author : fiv

from tag import Tag

from tokenn import Word


class Lexer:
    """
    Lexer是完成词法分析功能的类，数据成员line为行号，peek是向前的一个字符，words是符号表。成员函数reserve将给定记号加入符号表。它的构造函数(8至17行)将所有保留字加入符号表。
    """

    def __init__(self, sym_path, in_path):
        self.words = {}
        self.line = 1
        self.column = 0
        self.peek = ' '

        self.init_words(sym_path)
        self.text = open(in_path, 'r').read()
        self.index = 0
        self.max = len(self.text)
        # self.stack = []  # (bracket -> str, (line -> int, column -> int))
        self.tokens = []
        self.error = []  # (line -> int, column -> int, msg -> str)

    def analyze(self):
        while self.index < self.max:
            w = self.scan()
            if w is not None:
                self.tokens.append((w, (self.line, self.column - len(w.lexeme))))
        # self.check_error()

    def init_words(self, path):
        with open(path, 'r') as f:
            for line in f:
                t, v = line.split()
                self.reserve(Word(v, Tag(t)))

    def reserve(self, w: Word):
        self.words[w.lexeme] = w

    def readch(self):
        self.peek = self.text[self.index]
        self.index += 1
        self.column += 1
        # print(self.line, self.column, self.peek)

    def check_readch(self, c):
        self.readch()
        if self.peek != c:
            return False
        self.peek = ' '
        return True

    def scan_number(self) -> float:
        x = 0.0
        while True:
            x = x * 10 + int(self.peek)
            self.readch()
            if not self.peek.isdigit():
                break
        if self.peek != '.':
            return x
        x *= 10
        self.readch()
        d = 10
        while True:
            x += int(self.peek) / d
            d *= 10
            self.readch()
            if not self.peek.isdigit():
                break
        return x

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
                return Word("==", Tag.EQ)
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
            while self.peek != '\n':
                self.readch()
            return
        elif self.peek == '.':
            self.readch()
            if self.peek.isdigit():
                num = self.scan_number()
                return Word(str(num), Tag.REAL)
        elif self.peek == '(' or self.peek == ')' or self.peek == '[' or self.peek == ']' or self.peek == '{' or self.peek == '}':
            return self.scan_bracket()

        # digits
        if self.peek.isdigit():
            num = self.scan_number()
            if num.is_integer():
                return Word(str(int(num)), Tag.INT)
            return Word(str(num), Tag.REAL)

        # words
        if self.peek.isalpha():
            b = ""
            while True:
                b += self.peek
                self.readch()
                if not self.peek.isalpha():
                    break
            w = self.words.get(b)
            if w is not None:
                return w
            w = Word(b, Tag.UNKNOWN)
            self.error.append((self.line, self.column - len(b), f"unknown word {b}"))
            return w

    def error(self, line, column, msg):
        print(f"line {line}, column {column}: {msg}")

    # def check_error(self):
    #     if self.stack:
    #         for s, (r, c) in self.stack:
    #             self.error(r, c, f"unmatched bracket {s}")
    #     print("Lexical analysis completed")

    def output(self):
        print("{:<10} | {:<15} | {:<10} | {:<10}".format("lexeme", "tag", "row", "column"))
        print("-" * 50)
        for token, (r, c) in self.tokens:
            print("{:<10} | {:<15} | {:<10} | {:<10}".format(token.lexeme, token.tag.value, r, c))

        print("\n" + "-" * 50)
        if self.error:
            print("Error:")
            for r, c, msg in self.error:
                print(f"line {r}, column {c}: {msg}")


if __name__ == '__main__':
    from ENV import PATH

    sym_path = PATH.DATA_PATH / "work1" / "miniRC.sym"
    in_path = PATH.DATA_PATH / "work1" / "miniRC.in"

    lexer = Lexer(sym_path, in_path)
    lexer.analyze()
    lexer.output()

    # la.analyze()
    # print(la.tokens)

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
