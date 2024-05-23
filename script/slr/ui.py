# by fan
import numpy as np
import flet as ft
from slr import SLR
from grammar import EnumGrammar
from ENV import PATH

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


def app(page: ft.Page):
    # grammar
    with open('./grammar.txt', 'r') as f:
        grammar = f.readlines()
        grammar_table = ft.DataTable(
            width=2500,
            columns=[ft.DataColumn(ft.Text('Grammar'))],
            rows=[ft.DataRow(
                cells=[ft.DataCell(ft.Text(line))]
            ) for line in grammar]
        )
        grammar_table_cloumns = ft.Column(
            [
                ft.Container(
                    content=ft.Column([ft.Row([grammar_table], scroll=ft.ScrollMode.ALWAYS)],
                                      scroll=ft.ScrollMode.ALWAYS),
                    expand=2),
            ]
        )
        grammar_table_cloumns_area = ft.SafeArea(grammar_table_cloumns, expand=True)

    view_grammar = ft.View(
        "/grammar",
        [
            ft.AppBar(title=ft.Text("Grammar"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
            grammar_table_cloumns_area
        ]
    )

    # parsing
    page.scroll = ft.ScrollMode.ALWAYS
    term_list = []
    selected_files = ft.Text("No file selected")
    data_frame = np.full((100, 100), '', dtype='<U50')
    slr_area = None
    view_slr = ft.View(
        "/",
        [
            ft.AppBar(title=ft.Text("SLR"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row(
                [
                    ft.ElevatedButton("Go slr", on_click=lambda _: page.go("/slr_log")),
                    ft.ElevatedButton("Go dict", on_click=lambda _: page.go("/dict")),
                    ft.ElevatedButton("Go grammar", on_click=lambda _: page.go("/grammar")),
                ]
            ),
        ],
    )

    # def close_column():
    #     nonlocal slr_area
    #     if slr_area is not None:
    #         view_slr.controls.remove(slr_area)
    #         view_slr.update()
    #         slr_table = None  # 重置table变量

    def show_table():
        nonlocal data_frame, slr_area, selected_files, term_list
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
        slr_column = ft.Column(
            controls=[
                # ft.Container(
                #     content=ft.Row([pick_files_dialog, selected_files]),
                # ),
                ft.Container(
                    content=ft.Column([ft.Row([table], scroll=ft.ScrollMode.ALWAYS)], scroll=ft.ScrollMode.ALWAYS),
                    expand=2),
            ]
        )
        slr_area = ft.SafeArea(slr_column, expand=True)
        view_slr.controls.append(slr_area)

    def get_data():
        # nonlocal data_frame, term_list
        # selected_files.value = (
        #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # )
        # selected_files.update()
        # print(e.files[0].path)
        nonlocal data_frame, term_list
        path = PATH.DATA_PATH / "miniRC.in3"
        slr = SLR(path)

        # 获取终结符集和非终结符集
        for term in slr.non_term:
            term_list.append(term.value)
        for term in slr.term:
            term_list.append(term.value)

        # 填充数据
        data_frame = np.full((len(slr.lr.items), len(term_list)), '', dtype='<U50')
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
        show_table()

    get_data()

    # log
    data_frame_log = np.full((100, 2), '', dtype='<U50')
    selected_table = "slr_log"
    table_log_column_area = None

    table_dict = ft.DataTable(
        width=2500,
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
    table_dict_column = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column([ft.Row([table_dict], scroll=ft.ScrollMode.ALWAYS)], scroll=ft.ScrollMode.ALWAYS),
                expand=2),
        ]
    )
    table_dict_column_area = ft.SafeArea(table_dict_column, expand=True)

    view_log = ft.View(
        "/slr_log",
        [
            ft.AppBar(title=ft.Text("SLR_LOG"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row([
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False,
                    ),
                ),
                selected_files,
                ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
            ]),

        ],
    )

    def get_table_log_column_area():
        nonlocal table_log_column_area, data_frame_log
        print(data_frame_log)
        table_log = ft.DataTable(
            width=2500,
            columns=[
                ft.DataColumn(ft.Text("symbols")),
                ft.DataColumn(ft.Text("action"))
            ],
            rows=[ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(data_frame_log[i][0])),
                    ft.DataCell(ft.Text(data_frame_log[i][1]))
                ]
            ) for i in range(data_frame_log.shape[0])]
        )
        table_log_column = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([ft.Row([table_log], scroll=ft.ScrollMode.ALWAYS)], scroll=ft.ScrollMode.ALWAYS),
                    expand=2),
            ]
        )

        table_log_column_area = ft.SafeArea(table_log_column, expand=True)

    def show_log_column_area():
        nonlocal table_log_column_area, view_log
        view_log.controls.append(table_log_column_area)

    def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal data_frame_log, term_list, table_log_column_area
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        print(selected_files.value)
        path = PATH.DATA_PATH / selected_files.value
        slr = SLR(path)
        slr.process()
        with open("./slr_log.txt", "r") as f:
            lines = f.readlines()
            data_frame_log = np.full((len(lines), 2), '', dtype='U300')
            for i in range(len(lines)):
                flag = 0
                for j in range(len(lines[i])):
                    if flag == 0 and lines[i][j] == '\'':
                        flag = j
                        continue
                    if flag != 0 and lines[i][j] == '\'':
                        if lines[i][flag + 1:j] in abbreviations.keys():
                            data_frame_log[i][0] += abbreviations[lines[i][flag + 1:j]] + " "
                        else:
                            data_frame_log[i][0] += lines[i][flag + 1:j] + " "
                        flag = 0
                        continue
                    if lines[i][j:j + 6] == '] === ':
                        # data_frame[i][0] = lines[i][1:j]
                        data_frame_log[i][1] = lines[i][j + 6: -1]
        if table_log_column_area is not None:
            # print("remove")
            # print(data_frame_log)
            # print(table_log_column_area)
            view_log.controls.remove(table_log_column_area)
            table_log_column_area = None
        # print(table_log_column_area)
        get_table_log_column_area()
        show_log_column_area()
        view_log.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.extend([pick_files_dialog])

    def route_change(route):
        page.views.clear()
        page.views.append(
            view_slr
        ),
        if page.route == "/slr_log":
            page.views.append(
                view_log
            )

        elif page.route == "/dict":
            page.views.append(
                ft.View(
                    "/dict",
                    [
                        ft.AppBar(title=ft.Text("DICT"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        table_dict_column_area
                    ],
                )
            )
        elif page.route == "/grammar":
            page.views.append(
                view_grammar
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=app, view=ft.AppView.WEB_BROWSER)
