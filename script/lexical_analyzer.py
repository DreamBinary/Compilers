# -*- coding:utf-8 -*-
# @FileName : lexical_analyzer.py
# @Time : 2024/4/3 20:53
# @Author : fiv
from colorama import Fore, Back, Style


class LexicalAnalyzer:
    def __init__(self, text=None, file_path=None):
        assert text or file_path, 'text or file_path must be provided'
        if file_path:
            with open(file_path, 'r') as f:
                self.text = f.read()
        else:
            self.text = text
        self.index = 0
        self.tokens = []  # (token, value, row, column)
        self.row = 1
        self.column = 1
        self.last_column = 1
        self.colors = {
            'int': Fore.RED,
            'float': Fore.RED,
            'identifier': Fore.GREEN,
            'keyword': Fore.BLUE,
            'operator': Fore.MAGENTA,
            'separator': Fore.CYAN,
            'quote': Fore.YELLOW,
        }

    def output(self):
        # draw a table for tokens
        print(r"{:<15}  |  {:<15} |  {:<3} | {:<3}".format('Token', 'Value', 'Row', 'Column'))
        tr = 1
        for token in self.tokens:
            t, v, r, c = token
            if r != tr:
                print(Fore.WHITE, '-' * 50)
                tr = r
            print(self.colors[t] + "{:<15}  |  {:<15} |  {:<3} | {:<3}".format(t, v, r, c))

    def analyze(self):
        while self.index < len(self.text):
            self.last_column = self.column
            if self.is_space(self.text[self.index]):
                if self.text[self.index] == '\n':
                    self.row += 1
                    self.column = 0
                else:
                    self.column += 0
                self.add_index()
            elif self.is_digit(self.text[self.index]):
                self.analyze_digit()
            elif self.is_alpha(self.text[self.index]):
                self.analyze_alpha()
            elif self.is_operator(self.text[self.index]):
                self.analyze_operator()
            elif self.is_separator(self.text[self.index]):
                self.analyze_separator()
            elif self.is_comment(self.text[self.index]):
                self.analyze_comment()
            elif self.is_quote(self.text[self.index]):
                self.analyze_quote()
            else:
                self.index += 1
        return self.tokens

    def add_index(self, num=1):
        self.index += num
        self.column += num

    def analyze_digit(self):
        # 1e-3
        start = self.index
        while self.index < len(self.text) and (self.is_digit(self.text[self.index]) or self.text[self.index] == '.'):
            self.add_index()
        if self.text[self.index] == 'e':
            self.add_index()
            if self.text[self.index] == '+' or self.text[self.index] == '-':
                self.add_index()
            while self.index < len(self.text) and self.is_digit(self.text[self.index]):
                self.add_index()
        word = self.text[start:self.index]
        if '.' in word or 'e' in word:
            self.tokens.append(('float', word, self.row, self.last_column))
        else:
            self.tokens.append(('int', word, self.row, self.last_column))

    def analyze_alpha(self):
        start = self.index
        while self.index < len(self.text) and self.is_alnum(self.text[self.index]):
            self.add_index()
        word = self.text[start:self.index]
        if self.is_keyword(word):
            self.tokens.append(('keyword', word, self.row, self.last_column))
        else:
            self.tokens.append(('identifier', word, self.row, self.last_column))

    def analyze_operator(self):
        if self.text[self.index] == '+':
            if self.text[self.index + 1] == '+':
                self.tokens.append(('operator', '++', self.row, self.last_column))
                self.add_index(2)
            elif self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '+=', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '-':
            if self.text[self.index + 1] == '-':
                self.tokens.append(('operator', '--', self.row, self.last_column))
                self.add_index(2)
            elif self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '-=', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '*':
            if self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '*=', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '/':
            if self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '/=', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '%':
            if self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '%=', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '=':
            if self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '==', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '>':
            if self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '>=', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '<':
            if self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '<=', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '!':
            if self.text[self.index + 1] == '=':
                self.tokens.append(('operator', '!=', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()

        elif self.text[self.index] == '&':
            if self.text[self.index + 1] == '&':
                self.tokens.append(('operator', '&&', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        elif self.text[self.index] == '|':
            if self.text[self.index + 1] == '|':
                self.tokens.append(('operator', '||', self.row, self.last_column))
                self.add_index(2)
            else:
                self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
                self.add_index()
        else:
            self.tokens.append(('operator', self.text[self.index], self.row, self.last_column))
            self.add_index()

    def analyze_separator(self):
        self.tokens.append(('separator', self.text[self.index], self.row, self.last_column))
        self.add_index()

    def analyze_comment(self):
        if self.text[self.index + 1] == '/':
            while self.index < len(self.text) and self.text[self.index] != '\n':
                self.add_index()
        elif self.text[self.index + 1] == '*':
            self.add_index(2)
            while self.index < len(self.text) and not (
                    self.text[self.index] == '*' and self.text[self.index + 1] == '/'):
                self.add_index()
            self.add_index(2)

    def analyze_quote(self):
        quote = self.text[self.index]
        self.add_index()
        start = self.index
        while self.index < len(self.text) and not self.is_quote_end(self.text[self.index], quote):
            if self.is_quote_escape(self.text[self.index]):
                self.add_index()
            self.add_index()
        self.tokens.append(('quote', self.text[start:self.index], self.row, self.last_column))
        self.add_index()

    def is_digit(self, char):
        return '0' <= char <= '9'

    def is_alpha(self, char):
        return 'a' <= char <= 'z' or 'A' <= char <= 'Z'

    def is_alnum(self, char):
        return self.is_digit(char) or self.is_alpha(char)

    def is_space(self, char):
        return char == ' ' or char == '\n' or char == '\t'

    def is_operator(self, char):
        return char in ['+', '-', '*', '/', '%', '=', '>', '<', '!', '&', '|']

    def is_separator(self, char):
        return char in ['(', ')', '{', '}', '[', ']', ',', ';']

    def is_keyword(self, word):
        return word in ['if', 'else', 'while', 'for', 'int', 'float', 'double', 'char', 'void', 'return']

    def is_comment(self, char):
        return char == '/' and (self.text[self.index + 1] == '/' or self.text[self.index + 1] == '*')

    def is_quote(self, char):
        return char == '"' or char == "'"

    def is_quote_end(self, char, quote):
        return char == quote

    def is_quote_escape(self, char):
        return char == '\\'

    def is_quote_escape_end(self, char):
        return char == '\\'

    def is_quote_escape_quote(self, char):
        return char == '"' or char == "'"

    def is_quote_escape_n(self, char):
        return char == 'n'

    def is_quote_escape_t(self, char):
        return char == 't'

    def is_quote_escape_r(self, char):
        return char == 'r'


if __name__ == '__main__':
    text = r"""
struct node{
	int son[26];
	int mark;
}tire[1000005];
int num=0;
double i =-1.566*1e-3;
void insert(string s){
	int pos=0;
	for(int i=0;i<s.length();i++){
		int temp=s[i]-'a';
		if(!tire[pos].son[temp])
		tire[pos].son[temp]=++num;
		pos=tire[pos].son[temp];
	}
	tire[pos].mark++;
} 
bool find(string s){
	int pos=0;
	for(int i=0;i<s.length();i++){
		int temp=s[i]-'a';
		if(!tire[pos].son[temp])
		return 0;
		pos=tire[pos].son[temp];
	}
	if(tire[pos].mark)
	return 1;
	else
	return 0;
}
"""
    lexical_analyzer = LexicalAnalyzer(text)
    tokens = lexical_analyzer.analyze()
    lexical_analyzer.output()
