import flet as ft
import requests
from .login import login_view
    

class AdminView(ft.UserControl):
    
    def login(self):
        """Responsável por enviar as credenciais de login a API."""

        self.text_fields[-1].text = "Entrando..."
        self.text_fields[-1].disabled = True
        self.update()
        
        text_fields = self.text_fields[:len(self.text_fields) - 1]
        
        data = {
            "username": text_fields[0].value,
            "password": text_fields[1].value,
        }
        
        response = requests.post(
            url="http://django:8000/api/login/", 
            json=data
        )
        self.text_fields[-1].text = "Login"
        self.text_fields[-1].disabled = False
        self.update()
        
        response.status_code == 200
        if response.status_code != 200 and not self.page.client_storage.get("flet_frontend.auth_token"):
            
            self.page.banner.bgcolor=ft.colors.AMBER_100
            self.page.banner.leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40)
            self.page.banner.content=ft.Text(
                "Login está errado, por favor, inserir dados corretos!"
            )
            self.page.banner.open = True
            self.page.update()
            return

        login_view(page=self.page, data=response.json())
        
    
    def forms(self):
        """Responsável por criar o forms de login na página."""
        
        self.text_fields = []
        
        self.text_fields.append(
            ft.TextField(
                label="Usário",
                border_radius=ft.border_radius.all(20)
            )
        )
        
        self.text_fields.append(
            ft.TextField(
                label="Senha",
                border_radius=ft.border_radius.all(20),
                password=True,
                suffix=ft.IconButton(
                    icon=ft.icons.KEY_OUTLINED,
                    on_click=lambda e: self.show_password(e)
                )
            )
        )
        
        self.text_fields.append(
            ft.ElevatedButton(
                text="Login",
                bgcolor=ft.colors.GREEN,
                color=ft.colors.WHITE,
                on_click=lambda _: self.login(),
            )
        )
        
        return ft.Column(
            controls=self.text_fields,
            horizontal_alignment=ft.CrossAxisAlignment.END
        )
        
    def show_password(self, e):
        
        if self.text_fields[1].password:
            e.control.icon = ft.icons.KEY_OFF_ROUNDED
            self.text_fields[1].password = False
        else:
            e.control.icon = ft.icons.KEY_ROUNDED
            self.text_fields[1].password = True
            
        self.update()
        
    def build(self):
        
        return ft.Column(
            controls=[
                ft.Divider(),
                ft.Text(
                   value="Área do Administrator",
                   weight=ft.FontWeight.BOLD,
                   size=30
                   
                ),
                ft.Container(
                    content=self.forms(),
                    width=600,
                    bgcolor=ft.colors.WHITE,
                    padding=10,
                    border_radius=ft.border_radius.all(20),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.colors.BLUE_GREY_300,
                        offset=ft.Offset(0, 0),
                        blur_style=ft.ShadowBlurStyle.OUTER,
                    )
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )