# -*- coding:utf-8 -*-
# @FileName : tmp.py
# @Time : 2024/5/1 11:19
# @Author : fiv

from math import pow, e

a = [0, 1, 2]

a_e = [pow(e, i) for i in a]
a_e_s = sum(a_e)

mm = max(a) - min(a)
a_o = [i / mm for i in a]

m = sum(a) / len(a)
s = sum([(i - m) ** 2 for i in a]) / len(a)

print(a_e, a_e_s)
print(a_o, mm)
print(m, s)
print([i / a_e_s for i in a_e])
print([i / mm for i in a_o])
print([(i - m) / s for i in a])