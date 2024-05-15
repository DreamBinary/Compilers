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
        self.lr = LR()
        self.items: List[ItemCluster] = self.lr.items
        self.grammar = self.lr.grammar
        self.grammar_dict = self.convert_grammar_dict()
        self.term, self.non_term = self.split_sym(self.lr.sym)  # terminal, non-terminal
        self.dollar = "DOLLAR"
        self.epsilon = EnumGrammar.EPSILON
        self.first = self.get_first()
        self.follow = self.get_follow()

        self.midx = len(self.input)
        self.sym = []
        self.action = []

    def convert_grammar_dict(self):
        grammar_dict = defaultdict(list)
        for g in self.grammar:
            grammar_dict[g.pre].append(g.suf)
        return grammar_dict

    def split_sym(self, sym):
        term = []
        non_term = []
        for g in self.grammar:
            non_term.append(g.pre)
        for s in sym:
            if s not in non_term:
                term.append(s)
        return term, non_term

    def table(self):
        idx = 0
        state = 0
        while idx < self.midx:
            top = self.input[idx]
            idx += 1

            self.sym.append(top)

            print("state: ", state)
            print("top: ", top)

            n_state = self.items[state].get_goto(top[-1])
            if n_state is None:
                print("error")  # TODO
            elif n_state == -1:
                # 规约
                print("reduce")
            else:
                print("shift to ", n_state)

    def get_follow(self):
        follow = {nt: set() for nt in self.non_term}
        start = self.non_term[0]
        follow[start].add(self.dollar)

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

    def process(self):
        pass

    def get_input(self, input_file):
        pp = PreProcess(input_file)
        return pp.tokens


if __name__ == '__main__':

    import os
    from ENV import PATH

    path = PATH.DATA_PATH / "work2" / "miniRC.in1"
    slr = SLR(path)
    for g in slr.grammar:
        print(g.pre, g.suf)

    # TODO 检查一下
    print("==>> first")
    print(slr.first)
    print("==>> follow")
    print(slr.follow)
