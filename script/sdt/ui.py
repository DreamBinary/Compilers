# -*- coding:utf-8 -*-
# @FileName : ui.py
# @Time : 2024/6/8 21:36
# @Author : fiv

# by fan
import numpy as np
import flet as ft
from sdt import SDT
from grammar import EnumGrammar
from ENV import PATH


def app(page: ft.Page):
    # grammar
    selected_files = ft.Text("No file selected")
    the_table = None
    data_frame = []

    def show_table():
        nonlocal the_table, data_frame
        if the_table is not None:
            print("remove")
            page.remove(the_table)
        table = ft.DataTable(
            vertical_lines=ft.border.BorderSide(1, "black"),
            width=11000,
            columns=[ft.DataColumn(ft.Text("show"))],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(x))
                    ],
                )
                for x in data_frame]
        )
        page.add(table)

    # log
    selected_table = "file"

    def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal show_table
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        print(selected_files.value)
        path = PATH.DATA_PATH / selected_files.value
        sdt = SDT(path)
        sdt.parse()
        for l in sdt.get_code():
            data_frame.append(l)
        show_table()
        page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.extend([pick_files_dialog])
    selected_files = ft.Text()

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
                selected_files
            ]
        )
    )


if __name__ == '__main__':
    try:
        ft.app(target=app)
    except Exception as e:
        print(e)
