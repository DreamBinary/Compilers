# -*- coding:utf-8 -*-
# @FileName : lr.py
# @Time : 2024/5/12 20:06
# @Author : fiv

import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir))
sys.path.append(path)

from collections import defaultdict

from grammar import Grammar, EnumGrammar
from typing import Tuple, List
from copy import deepcopy
from tqdm import tqdm


class Item:
    def __init__(self, grammar: Tuple[EnumGrammar, Tuple], index: int, label):
        # pre -> suf
        self.label = label  # 标记在文法中的位置
        self.index = index
        self.pre = grammar[0]
        self.suf = grammar[1]

    def __eq__(self, other):
        if self.index != other.index:
            return False
        if self.pre != other.pre:
            return False
        if len(self.suf) != len(other.suf):
            return False
        for suf in self.suf:
            if suf not in other.suf:
                return False
        return True

    def end(self):
        return self.index >= len(self.suf)

    def current(self):
        if self.end():
            return None
        return self.suf[self.index]

    def __str__(self):
        a = self.suf[:self.index]
        b = self.suf[self.index:]
        if not a:
            a = ""
        else:
            a = " ".join([(i.value if type(i) is not str else i) for i in a])
        if not b:
            b = ""
        else:
            b = " ".join([(i.value if type(i) is not str else i) for i in b])
        return f"{self.pre.value} -> {a} . {b}"


class ItemCluster:
    def __init__(self, state: int, items: List[Item]):
        self.items = items
        self.state = state
        self.goto = defaultdict(lambda: -2)  # x -> state

    def get_goto(self, x):
        return self.goto.get(x)

    def get_reduce(self):
        r_items = []
        for i in self.items:
            if i.end():
                r_items.append(i)
        return r_items

    def __eq__(self, other):
        if len(self.items) != len(other.items):
            return False
        for i in self.items:
            if i not in other.items:
                return False
        return True

    def __bool__(self):
        return bool(self.items)

    def __str__(self):
        res = f"==>> state: {self.state}\n"
        for i in self.items:
            res += f"{i}  index: {i.index} {len(i.suf)}    goto: {self.goto[i.current()]}\n"
        r = self.get_reduce()
        for i in r:
            res += f"Reduce: {i.pre.value} -> {' '.join([j.value for j in i.suf])}\n"
        return res


# 文法分析
class LR:
    def __init__(self):
        self.grammar, self.sym = self.get_grammar()
        self.items = self.get_items()

    def goto(self, il, x):
        nil = []
        for i in il:
            if i.index < len(i.suf) and i.suf[i.index] == x:
                ii = deepcopy(i)
                ii.index += 1
                nil.append(ii)
        return self.closure(nil)

    def closure(self, il: List[Item]) -> List[Item]:
        j = il
        while True:
            flag = True
            for i in j:
                for g in self.grammar:
                    if g not in j:
                        cur = i.current()
                        if cur and cur.value == g.pre.value:
                            j.append(g)
                            flag = False
            if flag:
                break
        return j

    def get_items(self):
        bar = tqdm()
        state = 0
        c = [ItemCluster(state, self.closure([self.grammar[0]]))]
        state += 1
        now_len = 0
        while True:
            flag = True
            last_len = now_len
            now_len = len(c)
            for idx in range(last_len, now_len):
                for x in self.sym:
                    nic = ItemCluster(state, self.goto(c[idx].items, x))
                    if nic:
                        # ic x -> nic
                        if nic in c:
                            c[idx].goto[x] = c[c.index(nic)].state
                        else:
                            c.append(nic)
                            c[idx].goto[x] = nic.state
                            state += 1
                            bar.set_description(f"==>> state: {state}")
                            flag = False
                    else:
                        c[idx].goto[x] = -1

            if flag:
                break
        bar.set_description(f"==>> Done: {state}")
        bar.close()
        with open("LR0.txt", "w") as f:
            for i in c:
                f.write(str(i))
        return c

    def get_grammar(self):
        dirr = os.path.dirname(__file__)
        grammar = os.path.join(dirr, 'grammar.txt')
        g = Grammar(grammar)
        grammar, sym = g.get_grammar()
        grammar = [(Item(i, 0, idx) if i[1][0] != EnumGrammar.EPSILON else Item(i, 1, idx)) for idx, i in
                   enumerate(grammar)]
        return grammar, sym


if __name__ == "__main__":
    from ENV import PATH

    lr = LR()

    # TODO 检查LR0自动机
    with open("LR0.txt", "w") as f:
        for i in lr.items:
            print(i)
            f.write(str(i))
