# -*- coding:utf-8 -*-
# @FileName : sdt.py
# @Time : 2024/5/18 19:54
# @Author : fiv
from collections import defaultdict

from script.slr import SLR
from script.slr.grammar import EnumGrammar


class Mem:
    def __init__(self):
        self.type = None
        self.addr = None
        self.true = None
        self.false = None
        self.next = None
        self.value = None
        self.code = []


class SDT:
    """
    语法制导翻译 SLR(1) -> SDT
    """

    def __init__(self, input_file):
        self.todo = self.get_todo()  # 语义规则
        self.slr = SLR(input_file)
        self.sym, self.action = self.slr.process()
        self.grammar = self.slr.grammar
        self.top = -1
        self.stack = []
        self.addr = 100
        self.idx = 0
        self.idx_dict = defaultdict(lambda: None)
        self.var = {}  # 变量
        self.jump = defaultdict(lambda: None)
        self.identifier = "identifier"
        self.log = []

    def get_todo(self):
        with open("sdt.txt", 'r') as f:
            import re
            todo = f.read()
            # match { } 中间的内容
            todo = re.findall(r'\${(.*?)}\$', todo, re.DOTALL)
            todo = [t.strip() for t in todo]
            # for i, t in enumerate(todo):
            #     print(i, t)
        return todo

    def backpatch(self, arg1, arg2):
        self.jump[arg1] = arg2

    def gen(self, op, arg1=None, arg2=None):
        idx1, idx2 = None, None
        if arg1:
            idx1 = self.stack.index(arg1)
        if arg2:
            idx2 = self.stack.index(arg2)

        def add():
            self.idx_dict[self.addr] = self.idx
            self.idx += 1

        s = []
        if op == "LABEL":
            s.append(f"{self.addr} : {op}")
        elif op == "goto":
            if idx1 and self.stack[idx1].addr:
                s.append(f"{self.addr} : {op} {self.stack[idx1].addr}")
            else:
                addr = self.addr
                self.addr += 1
                return [f"{addr} : {op} {self.addr}"]
        elif op == "if":
            s.append(
                f"{self.addr} : if t{self.idx_dict[self.stack[idx1].true]} goto {self.jump[self.stack[idx1].true]}")
            self.addr += 1
            if self.stack[idx1].false:
                s.append(f"{self.addr} : goto {self.jump[self.stack[idx1].false]}")
            else:
                addr = self.addr
                self.addr += 1
                s.append(f"{addr} : goto {self.addr}")
                return s
        elif op == "var":
            if self.stack[idx1].value in self.var:
                return None
            self.var[self.stack[idx1].value] = self.addr
            self.stack[idx1].addr = self.addr  # 记录变量的地址
            self.idx_dict[self.addr] = self.idx
            s.append(f"{self.addr} : t{self.idx} = {op} {self.stack[idx1].value}")
            add()
        elif idx1 and idx2:
            s.append(
                f"{self.addr} : t{self.idx} = {self.idx_dict[self.stack[idx1].value]} {op} {self.idx_dict[self.stack[idx2].value]}")
            add()
        elif idx1:
            s.append(f"{self.addr} : t{self.idx} = {op} {self.stack[idx1].value}")
            add()
        self.addr += 1
        return s

    # def gen(self, op, arg1=None, arg2=None):
    #     # print("==>>", op, arg1, arg2)
    #     def add():
    #         self.idx_dict[self.addr] = self.idx
    #         self.idx += 1
    #
    #     if op == "LABEL":
    #         print("==>>", f"{self.addr} : {op}")
    #         self.log.append(f"{self.addr} : {op}")
    #     elif op.startswith("goto"):
    #         if op.endswith("if"):
    #             print("==>>", f"{self.addr} : if t{self.idx_dict[arg1]} goto {self.jump[arg1]}")
    #             self.log.append(f"{self.addr} : if t{self.idx_dict[arg1]} goto {self.jump[arg1]}")
    #         else:
    #             if arg1:
    #                 print("==>>", f"{self.addr} : {op} {arg1}")
    #                 self.log.append(f"{self.addr} : {op} {arg1}")
    #             else:
    #                 addr = self.addr
    #                 self.addr += 1
    #                 print("==>>", f"{addr} : {op} {self.addr}")
    #                 self.log.append(f"{addr} : {op} {self.addr}")
    #                 return addr
    #     elif op.startswith("var"):
    #         if arg1 in self.var:
    #             return self.var[arg1]
    #         self.var[arg1] = self.addr
    #         self.idx_dict[self.addr] = self.idx
    #         print("==>>", f"{self.addr} : t{self.idx} = {op} {arg1}")
    #         self.log.append(f"{self.addr} : t{self.idx} = {op} {arg1}")
    #         add()
    #     elif arg1 and arg2:
    #         if isinstance(arg1, int) and isinstance(arg2, int):
    #             print("==>>", f"{self.addr} : t{self.idx} = t{self.idx_dict[arg1]} {op} t{self.idx_dict[arg2]}")
    #             self.log.append(f"{self.addr} : t{self.idx} = t{self.idx_dict[arg1]} {op} t{self.idx_dict[arg2]}")
    #         else:
    #             print("==>>", f"{self.addr} : t{self.idx} = {arg1} {op} {arg2}")
    #             self.log.append(f"{self.addr} : t{self.idx} = {arg1} {op} {arg2}")
    #         add()
    #     elif arg1:
    #         print("==>>", f"{self.addr} : t{self.idx} = {op} {arg1}")
    #         self.log.append(f"{self.addr} : t{self.idx} = {op} {arg1}")
    #         add()
    #     addr = self.addr
    #     self.addr += 1
    #     return addr

    # def backpatch(self, arg1, arg2):
    #     print(f"backpatch: {arg1} {arg2}")

    def parse(self):
        #         self.stack.append(Mem())
        #         a = """
        #
        # self.stack[0].addr = self.gen('var', self.identifier)
        # print(self.stack[0].addr)
        #         """
        #         exec(a, {}, {'self': self})
        epsilon_idx = []
        for i, g in enumerate(self.grammar):
            if g.suf[0].value == EnumGrammar.EPSILON.value:
                epsilon_idx.append(i)
        print("==>> epsilon_idx", epsilon_idx)
        for (s, a) in zip(self.sym, self.action):
            if a[0].startswith("shift"):
                # print(f"shift: {a[1]}")
                self.stack.append(Mem())
                self.top += 1
                self.identifier = s[-1][0]
                # self.stack = s
            elif a[0].startswith("reduce"):
                # print(f"reduce: {self.grammar.index(a[1])} {a[1]}")
                index = self.grammar.index(a[1])
                if index in epsilon_idx:
                    self.stack.append(Mem())
                    self.top += 1
                code = self.get_exec(index)
                if code != "":
                    # print("===>>", "code", index)
                    # print(code)
                    self.log.append(str(index) + " -> " + str([s.addr for s in self.stack[:self.top + 1]]))
                    print(index)
                    exec(code, {}, {'self': self})
            else:
                raise ValueError(f"Unknown action: {a}")

    def get_exec(self, index):
        r = self.todo[index]
        replace = {
            # ';': '\n',
            'stack': 'self.stack',
            'top': 'self.top',
            'identifier': 'self.identifier',
            'gen': 'self.gen',
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
    for c in sdt.stack[sdt.top].code:
        print(c)
    print("==>> log")
    for l in sdt.log:
        print(l)

    print("==>> idx_dict")
    for k, v in sdt.idx_dict.items():
        print(k, v)
