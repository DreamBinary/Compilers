import flet as ft
import string


async def main(page: ft.Page):
    alphabets_upper = string.ascii_uppercase
    alphabets_lower = string.ascii_lowercase
    date_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Sl. No."), numeric=True),
            ft.DataColumn(ft.Text("Alphabet_Upper")),
            ft.DataColumn(ft.Text("Alphabet_Lower")),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True),
            ft.DataColumn(ft.Text("Simply a column"), numeric=True)
        ],
        rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(i + 1))),
                                ft.DataCell(ft.Text(alphabets_upper[i])),
                                ft.DataCell(ft.Text(alphabets_lower[i])),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i))),
                                ft.DataCell(ft.Text(str(i * i)))]) for i in range(len(alphabets_upper))]
    )
    column = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column([ft.Row([date_table], scroll=ft.ScrollMode.ALWAYS)], scroll=ft.ScrollMode.ALWAYS),
                expand=2),
            ft.Container(ft.Text('Anything'), expand=1),
            ft.Container(ft.Text('Anything'), expand=0)
        ]
    )
    await page.add_async(ft.SafeArea(column, expand=True))


ft.app(target=main)
