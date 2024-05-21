# -*- coding:utf-8 -*-
# @FileName : sdt.py
# @Time : 2024/5/21 8:21
# @Author : fiv

from collections import defaultdict

from script.slr import SLR
from script.slr.grammar import EnumGrammar


def debugprint(*args):
    print(*args)
    pass


class Mem:
    def __init__(self, value=None):
        self.type = None
        self.addr = None
        self.truelist = []
        self.falselist = []
        self.nextlist = []
        self.value = value
        self.instr = None


class SDT:
    """
    语法制导翻译 SLR(1) -> SDT
    """

    def __init__(self, input_file):
        self.todo = self.get_todo()  # 语义规则
        self.slr = SLR(input_file)
        self.sym, self.action = self.slr.process()
        self.grammar = self.slr.grammar

        self.nextinstr = 100
        self.table = defaultdict(lambda: None)  # 符号表
        self.type = None

        self.top = -1
        self.stack = []
        self.jump = defaultdict(lambda: None)

        self.idx = 0
        self.idx_dict = defaultdict(lambda: None)

        # self.log = []
        self.code = []

    def temp(self):
        self.idx += 1
        return f"t{self.idx}"

    def get_code(self):
        length = len(self.code)
        for i in range(length):
            if 'goto' in self.code[i]:
                instr = int(self.code[i].split(':')[0])
                self.code[i] = self.code[i] + str(self.jump[instr])
        return self.code

    def get_todo(self):
        with open("sdt.txt", 'r') as f:
            import re
            todo = f.read()
            todo = re.findall(r'\${(.*?)}\$', todo, re.DOTALL)
            todo = [t.strip() for t in todo]
        return todo

    def backpatch(self, arg1, arg2):
        for i in arg1:
            self.jump[i] = arg2

    def merge(self, arg1, arg2):
        result = arg1 + arg2
        print(result)

    def gen(self, op, arg1=None, arg2=None, result=None):
        debugprint("==>> gen", op, arg1, arg2)
        if op == 'if':
            s = f"{self.nextinstr}: if {arg1} goto "  # wait backpatch
            self.jump[self.nextinstr] = arg2
        elif op == 'goto':
            s = f"{self.nextinstr}: goto "
            self.jump[self.nextinstr] = arg1
        elif result:
            s = f"{self.nextinstr}: {result} = {arg1} {op} {arg2}"
        else:
            s = f"{self.nextinstr}: {arg1} {op} {arg2}"

        self.nextinstr += 1
        self.code.append(s)
        debugprint(s)
        return None

    def parse(self):
        epsilon_idx = []
        for i, g in enumerate(self.grammar):
            if g.suf[0].value == EnumGrammar.EPSILON.value:
                epsilon_idx.append(i)
        for (s, a) in zip(self.sym, self.action):
            if a[0].startswith("shift"):
                self.top += 1
                if len(self.stack) <= self.top:
                    self.stack.append(Mem(s[-1][0]))
                else:
                    self.stack[self.top] = Mem(s[-1][0])

                # self.stack = s
            elif a[0].startswith("reduce"):
                # debugprint(f"reduce: {self.grammar.index(a[1])} {a[1]}")
                index = self.grammar.index(a[1])
                if index in epsilon_idx:
                    self.top += 1
                    if len(self.stack) <= self.top:
                        self.stack.append(Mem(s[-1][0]))
                    else:
                        self.stack[self.top] = Mem(s[-1][0])
                code = self.get_exec(index)
                debugprint(index)
                if code != "":
                    # debugprint("===>>", "code", index)
                    # debugprint(code)
                    exec(code, {}, {'self': self})
            else:
                raise ValueError(f"Unknown action: {a}")
            debugprint(s)
            debugprint("==>> stack : ", [i.truelist for i in self.stack[:self.top + 1]])

    def get_exec(self, index):
        r = self.todo[index]
        replace = {
            # ';': '\n',
            'type': 'self.type',
            'table': 'self.table',
            'nextinstr': 'self.nextinstr',
            'stack': 'self.stack',
            'top': 'self.top',
            'gen': 'self.gen',
            'merge': 'self.merge',
            'temp': 'self.temp',
            'backpatch': 'self.backpatch',
        }
        for k, v in replace.items():
            r = r.replace(k, v)
        return r


if __name__ == '__main__':
    from ENV import PATH

    path = PATH.DATA_PATH / "tmp.in"

    sdt = SDT(path)
    sdt.parse()
    print("==>> code")
    for l in sdt.get_code():
        print(l)
    print("==>> jump")
    for k, v in sdt.jump.items():
        print(k, v)

    print("==>> idx_dict")
    for k, v in sdt.idx_dict.items():
        print(k, v)
