import flet as ft

def appbar(page: ft.Page):
    return ft.AppBar(
        leading=ft.Icon(ft.icons.ATTACH_MONEY),
        leading_width=40,
        title=ft.Text("Loans For Good"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.HOME, tooltip="Home", on_click=lambda _: page.go('/')),
            ft.IconButton(ft.icons.ADMIN_PANEL_SETTINGS, tooltip="Admin", on_click=lambda _: page.go('/admin')),
        ]
    )