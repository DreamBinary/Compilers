# -*- coding:utf-8 -*-
# @FileName : sym.py
# @Time : 2024/4/15 17:00
# @Author : fiv

class Symbol:
    def __init__(self, file_path):
        self.sym = {}
        self.from_file(file_path)

    def __str__(self):
        return str(self.sym)

    def get_type(self, value):
        return self.sym.get(value, None)

    def from_file(self, file_path):
        with open(file_path, "r") as file:
            for line in file:
                type, value = line.split()
                self.sym[value] = type


if __name__ == '__main__':
    from ENV import PATH

    path = PATH.DATA_PATH / "work1" / "miniRC.sym"
    s = Symbol(path)
    print(s)
