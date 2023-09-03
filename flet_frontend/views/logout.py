import flet as ft

def logout_view(page: ft.Page):
    """Responsável por alterar appbar e remover o token de login."""
        
    page.appbar.actions = [
        ft.IconButton(ft.icons.HOME, tooltip="Home", on_click=lambda _: page.go('/')),
        ft.IconButton(ft.icons.ADMIN_PANEL_SETTINGS, tooltip="Admin", on_click=lambda _: page.go('/admin')),
    ]
    page.client_storage.remove("flet_frontend.auth_token")
    page.go('/')
    page.update()