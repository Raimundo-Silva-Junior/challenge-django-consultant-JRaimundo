import flet as ft

from views import HomeView, AdminView, FormsView, ProposalsView


class Router:
    """Rotas do website."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {
            "/": HomeView(),
            "/admin": AdminView(),
            "/propostas": ProposalsView(page),
            "/forms": FormsView(),
            
        }
        self.body = ft.Container(content=self.routes['/'])

    def route_change(self, route):

        if not self.page.client_storage.get("flet_frontend.auth_token") and route.route not in ("/", "/admin"):
            self.page.banner.bgcolor=ft.colors.AMBER_100
            self.page.banner.leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40)
            self.page.banner.content=ft.Text(
                "Você deve estar logado como adm para acessar essa página."
            )
            self.page.banner.open = True
            self.page.update()
            return
        self.body.content = self.routes[route.route]
        self.body.update()