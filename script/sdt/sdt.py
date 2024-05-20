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
        self.var = {}
        self.jump = defaultdict(lambda: None)
        self.identifier = "identifier"

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
        # print("==>>", op, arg1, arg2)

        def add():
            self.idx_dict[self.addr] = self.idx
            self.idx += 1

        if op == "LABEL":
            print("==>>", f"{self.addr} : {op}")
        elif op.startswith("goto"):
            if op.endswith("if"):
                print("==>>", f"{self.addr} : if t{self.idx_dict[arg1]} goto {self.jump[arg1]}")
            else:
                if arg1:
                    print("==>>", f"{self.addr} : {op} {arg1}")
                else:
                    addr = self.addr
                    self.addr += 1
                    print("==>>", f"{addr} : {op} {self.addr}")
                    return addr
        elif arg1 and arg2:
            if isinstance(arg1, int) and isinstance(arg2, int):
                print("==>>", f"{self.addr} : t{self.idx} = t{self.idx_dict[arg1]} {op} t{self.idx_dict[arg2]}")
            else:
                print("==>>", f"{self.addr} : t{self.idx} = {arg1} {op} {arg2}")
            add()
        elif arg1:
            if op.startswith("var"):
                if arg1 in self.var:
                    return None
                self.var[arg1] = self.addr
                self.idx_dict[self.addr] = self.idx
                print("==>>", f"{self.addr} : t{self.idx} = {op} {arg1}")
                add()
            else:
                print("==>>", f"{self.addr} : t{self.idx} = {op} {arg1}")
                add()
        addr = self.addr
        self.addr += 1
        return addr

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
        epsilon_idx = [6, 12, 35, 62]
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
                # print("===>>", code)
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
