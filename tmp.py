# -*- coding:utf-8 -*-
# @FileName : ls.py
# @Time : 2024/5/16 13:53
# @Author : fiv

import turtle as t
from copy import deepcopy


class Draw:
    def __init__(self, angle, length):
        self.stack = []  # (pos, ang, len)
        self.length = length
        self.angle = angle

    def process(self, ls, cnt=3):
        tls = deepcopy(ls)
        for i in range(cnt):
            ls = ls.replace("F", tls)
        return ls

    def draw(self, ls, cnt=3, heading=None):
        nls = self.process(ls, cnt)
        t.penup()
        if heading:
            t.setheading(heading)
        t.goto(0, 0)
        t.pendown()
        for c in nls:
            if c == 'F':
                t.fd(self.length)
            elif c == '+':
                t.lt(self.angle)
            elif c == '-':
                t.rt(self.angle)
            elif c == '[':
                self.stack.append((t.pos(), t.heading(), self.length))
                self.length *= 0.6
            elif c == ']':
                pos, ang, length = self.stack.pop()
                self.length = length
                t.penup()
                t.goto(pos)
                t.setheading(ang)
                t.pendown()


if __name__ == '__main__':
    t.setup(800, 800)
    t.speed(0)
    lsl = [
        ("F+F+++F+F+++F", 60, 100),  # alpha = 60
        ("F[+F][-F]", 30, 100),  # alpha = 30
        ("[F[+F][-F]]", 30, 500),  # alpha = 30
    ]
    for ls, angle, length in lsl:
        t.reset()
        d = Draw(angle, length)
        d.draw(ls, cnt=5, heading=90)
        t.getcanvas().postscript(file=f'{ls}.eps')
    t.done()
# (1)
# w: F
# alpha: 60
# F -> F+F+++F+F+++F
# (2)
# w: F
# alpha: 30
# F -> F[+F][-F]
# (3)
# w: F
# alpha: 30
# F -> [F[+F][-F]]
#
#
# F[+F][-F][+F[+F][-F]][-F[+F][-F]]
