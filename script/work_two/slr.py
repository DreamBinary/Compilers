# -*- coding:utf-8 -*-
# @FileName : slr.py
# @Time : 2024/5/12 20:06
# @Author : fiv
from collections import defaultdict
from grammar import EnumGrammar
from lr import LR
from preprocess import PreProcess
from typing import List
from lr import ItemCluster


class SLR:
    def __init__(self, input_file):
        self.input = self.get_input(input_file)
        self.lr = LR()  # LR0自动机
        self.items: List[ItemCluster] = self.lr.items
        self.grammar = self.lr.grammar
        self.grammar_dict = self.convert_grammar_dict()
        self.sym = self.lr.sym
        self.term, self.non_term = self.split_sym(self.sym)  # terminal, non-terminal
        self.dollar = ("DOLLAR", "DOLLAR")  # 和sym保持一致
        self.epsilon = EnumGrammar.EPSILON
        self.first = self.get_first()
        self.follow = self.get_follow()

        self.midx = len(self.input)
        self.action = self.get_action()
        self.goto = self.get_goto()

    def process(self):
        # merge self.action and self.goto
        table = defaultdict(dict)
        for k, v in self.action.items():
            for kk, vv in v.items():
                table[k][kk] = vv
        for k, v in self.goto.items():
            for kk, vv in v.items():
                table[k][kk] = vv
        idx = 0
        stack = [0]
        symbols = [self.dollar[-1]]
        log_symbols = []
        log_action = []
        # print(self.action[3][EnumGrammar.IDENTIFIER])

        # print(table[8])
        # print(EnumGrammar.FUNCTION in table[8])
        cnt = 0
        while True:
            cnt += 1
            if idx >= self.midx:
                top = self.dollar
            else:
                top = self.input[idx]
            state = stack[-1]
            print("==>> stack")
            print(stack)
            print("==>> top")
            print(top)
            print("==>> state")
            print(state)
            print("==>> table[state]")
            print(table[state])
            print("==>> log_symbols")
            for sym, act in zip(log_symbols[-10:], log_action[-10:]):
                print(sym, "===", act)
            if top[-1] not in table[state]:
                print("==>> ERROR")
                print("idx", idx)
                print(top)
                print(self.input[idx - 1], top, self.input[idx + 1])
                print(state)
                print(table[state])
                print("====>>>> Log")
                for sym, act in zip(log_symbols[-10:], log_action[-10:]):
                    print(sym, "===", act)
                break
            action = table[state][top[-1]]
            if action == "acc":
                print("acc")
                break
            if action[0] == "s":
                next_state = int(action[1:])
                stack.append(next_state)
                symbols.append(top[0])
                log_symbols.append(symbols.copy())
                log_action.append(f"shift to {next_state}")
                idx += 1
            elif action[0] == "r":
                reduce = int(action[1:])
                grammar = self.grammar[reduce]
                if grammar.suf[0] != self.epsilon:
                    for _ in range(len(grammar.suf)):
                        stack.pop()
                        symbols.pop()
                state = stack[-1]
                if grammar.pre in table[state]:
                    next_state = table[state][grammar.pre]
                    stack.append(int(next_state[1:]))
                    symbols.append(grammar.pre.value)

                log_symbols.append(symbols.copy())
                log_action.append(f"reduce by {grammar.pre.value} -> {' '.join([str(i.value) for i in grammar.suf])}")
            # if cnt > 200:
            #     break
        return log_symbols, log_action

    def convert_grammar_dict(self):
        grammar_dict = defaultdict(list)
        for g in self.grammar:
            grammar_dict[g.pre].append(g.suf)
        return grammar_dict

    def split_sym(self, sym):
        term = set()
        non_term = set()
        for g in self.grammar:
            non_term.add(g.pre)
        for s in sym:
            if s not in non_term:
                term.add(s)
        return term, non_term

    def get_action(self):  # 分析表
        action = defaultdict(dict)
        il = len(self.items)
        sym = self.non_term.union(self.term).union({self.dollar[-1]})

        # 优先级
        priority = [
            EnumGrammar.ELIF, EnumGrammar.ELSE,  # if-else
            EnumGrammar.SEMI,  # ;
            EnumGrammar.EQ,  # = 连等的时候
            EnumGrammar.PLUS,
            EnumGrammar.MINUS,
            EnumGrammar.STAR,
            EnumGrammar.SLASH,
            EnumGrammar.LT,
            EnumGrammar.GT,
            EnumGrammar.LE,
            EnumGrammar.GE,
            EnumGrammar.EQEQ,
            EnumGrammar.NE,
            EnumGrammar.AND,
            EnumGrammar.OR,
            EnumGrammar.INC,
            EnumGrammar.DEC,
            EnumGrammar.LPAR,
            EnumGrammar.RPAR,
            EnumGrammar.LBRACE,
            EnumGrammar.RBRACE,
            EnumGrammar.LSQB,
            EnumGrammar.RSQB,
            EnumGrammar.COMMA,
            EnumGrammar.SEMI,
            EnumGrammar.DOT,
            EnumGrammar.COMMENT,
        ]

        for idx in range(il):
            item = self.items[idx]
            state = item.state
            for s in sym:
                goto = item.get_goto(s)
                if goto:
                    if goto == -1:
                        reduce = item.get_reduce()
                        if reduce:
                            for r in reduce:
                                if r.pre == EnumGrammar.PROGRAM_:
                                    action[state][self.dollar[-1]] = "acc"
                                else:
                                    for f in self.follow[r.pre]:
                                        # if action[state].get(f):
                                        #     continue
                                        if ((f in priority) and action[state].get(f) and
                                                action[state][f][0] == 's'):  # 处理优先级
                                            continue
                                        action[state][f] = f"r{r.label}"
                    else:
                        action[state][s] = f"s{goto}"
        return action

    def get_goto(self):
        goto = defaultdict(dict)
        il = len(self.items)
        for idx in range(il):
            item = self.items[idx]
            state = item.state
            for s in self.non_term:
                goto_state = item.get_goto(s)
                if goto_state and goto_state != -1:
                    goto[state][s] = f"s{goto_state}"
        return goto

    def get_follow(self):
        follow = {nt: set() for nt in self.non_term}
        start = EnumGrammar.PROGRAM_
        follow[start].add(self.dollar[-1])
        while True:
            flag = False
            for lhs in self.grammar_dict:
                for product in self.grammar_dict[lhs]:
                    trailer = follow[lhs].copy()
                    for sym in reversed(product):
                        if sym in self.grammar_dict:
                            if follow[sym] != follow[sym].union(trailer):
                                follow[sym].update(trailer)
                                flag = True
                            if self.epsilon in self.first[sym]:
                                trailer = trailer.union(self.first[sym] - {self.epsilon})
                            else:
                                trailer = self.first[sym]
                        else:
                            trailer = {sym}
            if not flag:
                break
        return follow

    def get_first(self):
        first = {nt: set() for nt in self.non_term}

        def first_of(sym):
            if sym not in self.grammar_dict:
                return {sym}
            if sym in first and first[sym]:
                return first[sym]
            for pro in self.grammar_dict[sym]:
                if pro[0] == self.epsilon:
                    first[sym].add(self.epsilon)
                else:
                    for p in pro:
                        if p == sym:
                            continue
                        result = first_of(p)
                        first[sym].update(result - {self.epsilon})
                        if self.epsilon not in result:
                            break
                        else:
                            first[sym].add(self.epsilon)
            return first[sym]

        for nt in self.non_term:
            first_of(nt)

        return first

    def get_input(self, input_file):
        pp = PreProcess(input_file)
        return pp.tokens


if __name__ == '__main__':
    from ENV import PATH

    path = PATH.DATA_PATH / "work2" / "miniRC.in1"
    slr = SLR(path)
    log_symbols, log_action = slr.process()
    print("==>> non_term")
    print(slr.non_term)
    print("==>> term")
    print(slr.term)
    print("==>> log")
    for sym, act in zip(log_symbols[-10:], log_action[-10:]):
        print(sym, "===", act)

    # for g in slr.grammar:
    #     print(g.pre, g.suf)

    # TODO 检查一下
    print("==>> first")
    print("==>> follow")
    print(slr.follow)
    print("-----------------", slr.grammar_dict[EnumGrammar.FUNCTION])
    print("==>> action")
    for k, v in slr.action.items():
        for kk, vv in v.items():
            print(k, kk, vv)
    print("==>> goto")
    for k, v in slr.goto.items():
        for kk, vv in v.items():
            print(k, kk, vv)
