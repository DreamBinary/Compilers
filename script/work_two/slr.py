# -*- coding:utf-8 -*-
# @FileName : slr.py
# @Time : 2024/5/12 20:06
# @Author : fiv

from lr import LR
from preprocess import PreProcess
from typing import List
from lr import ItemCluster


class SLR:

    def __init__(self, input_file):
        self.input = self.get_input(input_file)
        self.items = self.get_items()
        self.midx = len(self.input)
        self.sym = []
        self.action = []

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

    def process(self):
        pass

    def get_items(self) -> List[ItemCluster]:
        lr = LR()
        return lr.items

    def get_input(self, input_file):
        pp = PreProcess(input_file)
        return pp.tokens


if __name__ == '__main__':
    import os
    from ENV import PATH

    path = PATH.DATA_PATH / "work2" / "miniRC.in1"
    slr = SLR(path)
    slr.process()
