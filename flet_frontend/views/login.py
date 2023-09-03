import flet as ft
from .logout import logout_view
import requests

def login_view(page: ft.Page, data: dict):
    """Responsável por alterar appbar e salvar o token de login."""
    
    page.client_storage.set("flet_frontend.auth_token", data)
        
    page.appbar.actions = [
        ft.IconButton(ft.icons.CONTACT_PAGE, tooltip="Forms", on_click=lambda _: page.go('/forms')),
        ft.IconButton(ft.icons.MENU_BOOK, tooltip="Propostas", on_click=lambda _: page.go('/propostas')),
        ft.IconButton(ft.icons.LOGOUT, tooltip="Logout", on_click=lambda _: logout_view(page)),
    ]
    
    page.go("/forms")
    
    page.update()