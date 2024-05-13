# -*- coding:utf-8 -*-
# @FileName : grammar.py
# @Time : 2024/5/12 21:00
# @Author : fiv


from enum import Enum
import re

"""
miniRC=function(integer delta){
     integer a[5] [10], b[5] [10], i, j;
     for(i=0; i<5; i++) for(j=0; j<10; j++){
		a[i] [j] = i + j;
                if(i>j) b[i] [j]=i*delta+j; else b[i] [j]=i-j/delta;
     }
     integer sum;
     sum = i = j = 0;
     repeat{
        if (i>j){
           j++;
           sum--;
        }else i++;
        if(i<5 && j<10) sum = sum + a[i] [j]*b[i] [j]; else break;
    }until(sum>=100);
    return(sum);
}
"""

"""
miniRC=function(integer N, integer K, double rc){
     integer a[10] [20];
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
"""

"""
grammar:


type -> integer | double | epsilon
program -> function | variable
variable -> type identifier | 
            type identifier = expression |  
            type identifier = function |
            type identifier , variable |
            type identifier [ integer ] |
            type identifier [ integer ] [ integer ] 
# function -> type identifier ( ) { statement } | type identifier ( ) |
#             type identifier ( variable ) { statement } | type identifier ( variable ) | 
#             type identifier ( variable , variable ) { statement } |  type identifier ( variable , variable ) |
#             type identifier ( variable , variable , variable ) { statement } | 
#             type identifier ( variable , variable , variable )

function -> type identifier ( ) { statement } | type identifier ( ) |
            type identifier ( expression ) { statement } | type identifier ( expression ) | 
            type identifier ( expression , expression ) { statement } |  type identifier ( expression , expression ) |
            type identifier ( expression , expression , expression ) { statement } | 
            type identifier ( expression , expression , expression )


statement -> variable ; | 
             if ( expression ) statement | 
             if ( expression ) statement else statement |
             if ( expression ) statement else if ( expression ) statement |
             repeat { statement } until ( expression ) |
             for ( expression ; expression ; expression ) { statement } |
             for ( expression ; expression ; expression ) statement |
             return expression ; |
             comment statement |
             statement statement |
             break |
             epsilon | ;
             

expression -> variable | function |
              expression + expression | expression - expression | 
              expression * expression | expression / expression |
              expression < expression | expression > expression | 
              expression == expression | expression != expression | 
              expression && expression | expression || expression |
              expression ++ | expression -- |
              ( expression )

digit -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
int -> digit | digit int
float -> int . int | . int | int .
letter -> a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z |
            A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z
identifier -> letter | letter identifier | letter digit | letter digit identifier
comment -> # | # letter | # letter comment | # digit | # digit comment | # digit letter | # digit letter comment
"""


class EnumGrammar(Enum):
    TYPE = 'TYPE'
    PROGRAM = 'PROGRAM'
    VARIABLE = 'VARIABLE'
    FUNCTION = 'FUNCTION'
    STATEMENT = 'STATEMENT'
    EXPRESSION = 'EXPRESSION'
    DIGIT = 'DIGIT'
    INTEGER = 'INTEGER'
    INT = 'INT'
    DOUBLE = 'DOUBLE'
    FLOAT = 'FLOAT'
    LETTER = 'LETTER'
    IDENTIFIER = 'IDENTIFIER'
    COMMENT = 'COMMENT'
    IF = 'IF'
    ELSE = 'ELSE'
    REPEAT = 'REPEAT'
    UNTIL = 'UNTIL'
    FOR = 'FOR'
    BREAK = 'BREAK'
    RETURN = 'RETURN'
    EPSILON = 'EPSILON'


class EnumSymbol(Enum):
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


class Grammar:
    def __init__(self, grammar: str):
        self.grammar = grammar
        self.grammar_dict = self.covert_grammar()

    def covert_grammar(self):
        # covert grammar to dict, str
        tmp_grammar_dict = {}
        for line in self.grammar.split('\n'):
            if not line:
                continue
            key, value = line.split('->')
            key = key.strip()
            value = value.strip()
            # split by '|' not ' ||'
            value = re.split(r'\s*\|\s*', value)
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
                            nv.append(EnumSymbol(vv))
                        elif len(vv) == 1:
                            nv.append(str(vv))
                        else:
                            # convert value to EnumGrammar
                            nv.append(EnumGrammar(vv.upper()))
                new_value.append(tuple(nv))
            for tv in new_value:
                new_grammar_dict.append((new_key, tv))
        return new_grammar_dict


if __name__ == '__main__':
    grammar = r"""
type -> integer | double | epsilon
program -> function | variable
variable -> type identifier | type identifier = expression | type identifier = function | type identifier , variable | type identifier [ integer ] | type identifier [ integer ] [ integer ] 
function -> type identifier ( ) { statement } | type identifier ( ) | type identifier ( expression ) { statement } | type identifier ( expression ) |  type identifier ( expression , expression ) { statement } |  type identifier ( expression , expression ) | type identifier ( expression , expression , expression ) { statement } | type identifier ( expression , expression , expression )
statement -> variable ; |  if ( expression ) statement |  if ( expression ) statement else statement | if ( expression ) statement else if ( expression ) statement | repeat { statement } until ( expression ) | for ( expression ; expression ; expression ) { statement } | for ( expression ; expression ; expression ) statement | return expression ; | comment statement | statement statement | epsilon | ; | break
expression -> variable | function | expression + expression | expression - expression | expression * expression | expression / expression | expression < expression | expression > expression | expression == expression | expression != expression | expression && expression | expression || expression | expression ++ | expression -- | ( expression )
digit -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
int -> digit | digit int
float -> int . int | . int | int .
letter -> a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z
identifier -> letter | letter identifier | letter digit | letter digit identifier
comment -> # | # letter | # letter comment | # digit | # digit comment | # digit letter | # digit letter comment
"""
    g = Grammar(grammar)
    grammar_dict = g.covert_grammar()

    # TODO: print grammar_dict
    # for k, v in grammar_dict.items():
    #     print(k, " -> ", end='')
    #     for vv in v:
    #         print(vv, end=' | ')
    #         # print(tuple([(vvv.value if type(vvv) is not str else vvv) for vvv in vv]), end=' | ')
    #     print()
    for i in grammar_dict:
        print(i)
