from slr import SLR
from grammar import EnumGrammar
import numpy as np
import pandas as pd
import sys
import os
from ENV import PATH

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)

path = PATH.DATA_PATH / "miniRC.in3"
slr = SLR(path)

# 获取终结符集和非终结符集
term_list = []
for term in slr.non_term:
    term_list.append(term.value)
for term in slr.term:
    term_list.append(term.value)
print(term_list)
data_frame = np.full((len(slr.lr.items), len(term_list)), '', dtype='<U50')

# 填充数据
for state, action in slr.action.items():
    for term, act in action.items():
        if type(term) == EnumGrammar:
            data_frame[state][term_list.index(term.value)] = act
            continue
        if term == '$':
            continue
        data_frame[state][term_list.index(term)] = act

for state, goto in slr.goto.items():
    for term, act in goto.items():
        if type(term) == EnumGrammar:
            data_frame[state][term_list.index(term.value)] = act
        else:
            data_frame[state][term_list.index(term)] = act

# 画图
import flet as ft


async def app(page: ft.Page):
    page.window_width = 13200
    table = ft.DataTable(
        vertical_lines=ft.border.BorderSide(1, "black"),
        width=11000,
        columns=[ft.DataColumn(ft.Text(term), numeric=True) for term in ['state'] + term_list],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(i)))] + [
                    ft.DataCell(ft.Text(data_frame[i][j])) for j in range(data_frame.shape[1])
                ],
            )
            for i in range(data_frame.shape[0])]

    )
    column = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column([ft.Row([table], scroll=ft.ScrollMode.ALWAYS)], scroll=ft.ScrollMode.ALWAYS),
                expand=2),
        ]
    )
    page.add(ft.SafeArea(column, expand=True))


ft.app(target=app)
