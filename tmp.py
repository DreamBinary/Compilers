import flet as ft
import string

import flet as ft


def main(page: ft.Page):
    page.title = "Routes Example"
    s = "HELLO"

    text = ft.Text("Hello world")

    def on_click(_):
        global s

        view.controls.append(text)
        page.go("/store")

    view = ft.View(
        "/store",
        [
            ft.ElevatedButton(f"{s}", on_click=lambda _: page.go("/")),
        ],
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("GO", on_click=on_click),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                view
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
