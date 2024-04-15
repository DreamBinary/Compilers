# -*- coding:utf-8 -*-
# @FileName : tmp.py
# @Time : 2024/4/6 14:08
# @Author : fiv


from pathlib import Path

path = Path("X:\yyyyyyyyyy\yjjj_sort\竞赛")

with open(path.parent / "ZZZ.txt", "w") as file:
    for f in path.glob("*"):
        t = f.stem
        print(t)
        file.write("".join(t) + "\n")
