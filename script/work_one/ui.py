# -*- coding:utf-8 -*-
# @FileName : ui.py
# @Time : 2024/4/16 20:43
# @Author : fiv


import flet as ft
from lexer import Lexer
from pathlib import Path


def process(file_path: str):
    lexer = Lexer(Path(file_path))
    tokens, symtable, error = lexer.analyze()
    lexer.output()
    lexer.output_symtable()
    lexer.output_error()
    return tokens, symtable, error


def app(page: ft.Page):
    tokens, symtable, error = [], {}, []
    page.scroll = "always"
    page.window_width = 1200
    token_data_table = None
    symtable_data_table = None
    error_data_table = None
    selected_table = "token_table"

    def get_token_data_table():
        return ft.DataTable(
            width=1200,
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

    def get_symtable_data_table():
        return ft.DataTable(
            width=1200,
            columns=[
                ft.DataColumn(ft.Text("lexeme")),
                ft.DataColumn(ft.Text("tag"))
            ],
            # for tag, lexemes in self.symtable.items():
            rows=[ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(lexeme)),
                    ft.DataCell(ft.Text(tag))
                ],
            ) for tag, lexemes in symtable.items() for lexeme in lexemes]
        )

    def get_error_data_table():
        return ft.DataTable(
            width=1200,
            columns=[
                ft.DataColumn(ft.Text("row")),
                ft.DataColumn(ft.Text("column")),
                ft.DataColumn(ft.Text("error")),
            ],
            rows=[ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(r)),
                    ft.DataCell(ft.Text(c)),
                    ft.DataCell(ft.Text(e)),
                ],
            ) for r, c, e in error]
        )

    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        print(e.files[0].path)
        nonlocal tokens, symtable, token_data_table, symtable_data_table, error
        tokens, symtable, error = process(e.files[0].path)

        if selected_table == "token_table":
            show_token_table()
        else:
            show_symtable_table()

    def clean():
        nonlocal token_data_table, symtable_data_table, error_data_table
        if token_data_table is not None:
            page.remove(token_data_table)
            token_data_table = None
        if symtable_data_table is not None:
            page.remove(symtable_data_table)
            symtable_data_table = None
        if error_data_table is not None:
            page.remove(error_data_table)
            error_data_table = None

    def show_token_table():
        nonlocal token_data_table
        clean()
        token_data_table = get_token_data_table()
        page.add(token_data_table)

    def show_symtable_table():
        nonlocal symtable_data_table
        clean()
        symtable_data_table = get_symtable_data_table()
        page.add(symtable_data_table)

    def change_table():
        nonlocal selected_table, selected_table_btn
        if selected_table == "token_table":
            show_symtable_table()
            selected_table = "symtable_table"
        else:
            show_token_table()
            selected_table = "token_table"
        selected_table_btn.text = selected_table
        selected_table_btn.update()

    def show_error():
        nonlocal error_data_table
        clean()
        error_data_table = get_error_data_table()
        page.add(error_data_table)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_table_btn = ft.ElevatedButton(
        selected_table,
        on_click=lambda _: change_table()
    )
    error_btn = ft.ElevatedButton(
        "error",
        on_click=lambda _: show_error()
    )
    selected_files = ft.Text()

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog])

    page.title = '词法分析器'

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False,
                    ),
                ),
                selected_table_btn,
                error_btn,
                selected_files,
            ]
        )
    )


if __name__ == '__main__':
    try:
        ft.app(target=app)
    except Exception as e:
        print(e)
        raise e
