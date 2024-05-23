# by fan
import numpy as np
import flet as ft

abbreviations = {
    'TYPE': 'TY',
    'EXPRESSIONLISTVAR': 'EX',
    'ASSIGN': 'AS',
    'COMPUTEEXPR': 'CO',
    'COMPAREEXPR': 'CM',
    'INDEX': 'IN',
    'EXPRESSION': 'EP',
    'BOOLEXPR': 'BO',
    'PARTEXPR': 'PA',
    'VARIABLE': 'VA',
    'IFBLOCK': 'IF',
    'PROGRAM': 'PR',
    'FUN': 'FUN',
    'ELIFSTMT': 'EL',
    'STATEMENTNO': 'ST',
    'IFSTMT': 'IS',
    'EXPRESSIONLIST': 'ER',
    'STATEMENTLIST': 'SA',
    'CONDITION': 'CN',
    'STATEMENT': 'SE',
    'PROGRAM_': 'PO',
    'ELSEIF': 'ES',
    'REPEAT': 'RE',
    '>=': '>=',
    ')': ')',
    'UNTIL': 'UN',
    '*': '*',
    'IDENTIFIER': 'ID',
    'LABEL': 'LA',
    '&&': '&&',
    'BREAK': 'BR',
    '-': '-',
    '/': '/',
    '+': '+',
    '=': '=',
    ',': ',',
    'DOUBLE': 'DO',
    '||': '||',
    'INTEGER': 'IT',
    'GOTOLABEL': 'GO',
    '<=': '<=',
    'INT': 'INT',
    'ELSE': 'EE',
    '#': '#',
    'FUNCTION': 'FU',
    'RETURN': 'RT',
    '}': '}',
    '[': '[',
    'FOR': 'FOR',
    'IF': 'IF',
    'EPSILON': 'EI',
    ';': ';',
    '>': '>',
    '--': '--',
    '!=': '!=',
    '==': '==',
    '.': '.',
    '++': '++',
    '(': '(',
    '$': '$',
    '{': '{',
    'FLOAT': 'FL',
    '<': '<',
    'WHILE': 'WH',
    ']': ']'
}
with open("./slr_log.txt", "r") as f:
    lines = f.readlines()
    data_frame = np.full((len(lines), 2), '', dtype='U300')
    for i in range(len(lines)):
        flag = 0
        for j in range(len(lines[i])):
            if flag == 0 and lines[i][j] == '\'':
                flag = j
                continue
            if flag != 0 and lines[i][j] == '\'':
                if lines[i][flag + 1:j] in abbreviations.keys():
                    data_frame[i][0] += abbreviations[lines[i][flag + 1:j]] + " "
                else:
                    data_frame[i][0] += lines[i][flag + 1:j] + " "
                flag = 0
                continue
            if lines[i][j:j + 6] == '] === ':
                # data_frame[i][0] = lines[i][1:j]
                data_frame[i][1] = lines[i][j + 6: -1]
    print(data_frame)


    def app(page: ft.Page):
        page.window_width = 1000
        page.scroll = "always"
        selected_table = "slr_log"
        table = ft.DataTable(
            width=800,
            columns=[
                ft.DataColumn(ft.Text("symbols")),
                ft.DataColumn(ft.Text("action"))
            ],
            rows=[ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(data_frame[i][0])),
                    ft.DataCell(ft.Text(data_frame[i][1]))
                ]
            ) for i in range(data_frame.shape[0])]
        )

        table1 = ft.DataTable(
            width=800,
            columns=[
                ft.DataColumn(ft.Text("symbols")),
                ft.DataColumn(ft.Text("identification"))
            ],
            rows=[ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(key)),
                    ft.DataCell(ft.Text(value))
                ]
            ) for key, value in abbreviations.items()]
        )

        def change_table():
            nonlocal selected_table, selected_table_btn
            if selected_table == "slr_log":
                page.remove(table)
                selected_table = "map_table"
                page.add(table1)
            else:
                page.remove(table1)
                selected_table = "slr_log"
                page.add(table)
            selected_table_btn.text = selected_table
            selected_table_btn.update()

        selected_table_btn = ft.ElevatedButton(
            selected_table,
            on_click=lambda _: change_table()
        )
        page.add(
            ft.Row(
                [
                    selected_table_btn,
                ]
            )
        )
        page.add(table)

if __name__ == '__main__':
    ft.app(target=app)
