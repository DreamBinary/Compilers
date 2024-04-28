# -*- coding:utf-8 -*-
# @FileName : ui.py
# @Time : 2024/4/16 20:43
# @Author : fiv


import flet as ft
from lexer import Lexer


def process(file_path: str):
    lexer = Lexer(file_path)
    tokens, symtable = lexer.analyze()
    lexer.output()
    lexer.output_symtable()
    return tokens, symtable


def app(page: ft.Page):
    tokens,symtable = [],[]
    page.scroll = "always"
    page.window_width = 1200


    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        print(e.files[0].path)
        nonlocal tokens,symtable,dataTable
        tokens,symtable = process(e.files[0].path)

        page.remove(dataTable)

        dataTable = ft.DataTable(
            width=1200,
            height=2000,
            columns=[
                ft.DataColumn(ft.Text("lexeme")),
                ft.DataColumn(ft.Text("tag")),
                ft.DataColumn(ft.Text("row")),
                ft.DataColumn(ft.Text("column"))
            ],
            rows=[ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(token.lexeme)),
                    ft.DataCell(ft.Text(token.tag.value)),
                    ft.DataCell(ft.Text(r)),
                    ft.DataCell(ft.Text(c)),
                ],
            ) for token, (r, c) in tokens]
        )

        page.add(dataTable)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()


    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog])

    page.title = '词法分析器'

    dataTable = ft.DataTable(
            width=1200,
            height=2000,
            # column_spacing=200,
            columns=[
                ft.DataColumn(ft.Text("lexeme")),
                ft.DataColumn(ft.Text("tag")),
                ft.DataColumn(ft.Text("row")),
                ft.DataColumn(ft.Text("column"))
            ],
            rows=[ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(token.lexeme)),
                        ft.DataCell(ft.Text(token.tag.value)),
                        ft.DataCell(ft.Text(r)),
                        ft.DataCell(ft.Text(c)),
                    ],
                ) for token, (r, c) in tokens]
        )

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                selected_files,
            ]
        ),
        dataTable
    )

    # get file path

    # process

    # show result in table


if __name__ == '__main__':
    ft.app(target=app)
