import flet as ft
from routers import Router
from appbar import appbar
from views import login_view
import requests
 

def main(page: ft.Page):
    """Arquivo principal, responsável por iniciar o fronend."""
    page.theme_mode = ft.ThemeMode.LIGHT
    def close_banner(e):
        page.banner.open = False
        page.update()
        
    page.banner = ft.Banner(
        bgcolor=None,
        leading=None,
        content=ft.Text(
            ""
        ),
        actions=[
            ft.TextButton("Ok", on_click=close_banner),
        ],
    )
    
    page.appbar = appbar(page)
    
    router = Router(page)

    page.on_route_change = router.route_change
    
    page.add(
        router.body
    )

    if page.client_storage.get("flet_frontend.auth_token"):

        response = requests.get(
            "http://django:8000/api/proposal/data/", 
            {"Authorization": f"Bearer {page.client_storage.get('flet_frontend.auth_token')['access']}"}
        )

            
        if response.status_code != 200:
            page.go("/")
        else:
            login_view(page, data=page.client_storage.get("flet_frontend.auth_token"))

      
ft.app(
    target=main,
    view=ft.WEB_BROWSER,
    port=7000
)