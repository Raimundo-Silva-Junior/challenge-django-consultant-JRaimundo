
import flet as ft
import requests
    

class FormsView(ft.UserControl):
    
    def fetch_proposal_model(self):
        """Responsável por colerar modelo de proposta."""
        
        response = requests.get(
            url="http://django:8000/api/proposal_model/get/1/"
        )
        return response.json()
    
    def send_forms(self):
        """Responsável por enviar o forms modificado para a API."""

        self.text_fields[-1].text = "Salvando..."
        self.text_fields[-1].disabled = True
        self.update()
        
        
        data = {
            "proposal_name": 'Modelo de Proposta',
            "content": {},
        }

        for control in self.forms_column.controls[1::]:
            if isinstance(control, ft.Row): 
                data["content"].update({control.controls[0].label: "Descrição..." })
        
        self.text_fields[-1].text = "Salvar"
        self.text_fields[-1].disabled = False
        self.update()

        
        response = requests.put(
            url="http://django:8000/api/proposal_model/change/1/",
            headers={"Authorization": f"Bearer {self.page.client_storage.get('flet_frontend.auth_token')['access']}"},
            json=data,
        )

        if response.status_code == 401:
            self.page.client_storage.remove('flet_frontend.auth_token')
            self.page.go("/admin")  
            return 

        if response.status_code != 200:
            
            self.page.banner.bgcolor=ft.colors.AMBER_100
            self.page.banner.leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40)
            self.page.banner.content=ft.Text(
                "Não foi possível salvar as informação, tente novamente.... "
            )
            self.page.banner.open = True
            self.page.update()
            return
        
        self.page.banner.bgcolor=ft.colors.GREEN_100
        self.page.banner.leading=ft.Icon(ft.icons.APPROVAL, color=ft.colors.GREEN, size=40)
        self.page.banner.content=ft.Text(
            "Informações salvas com sucesso!"
        )
        self.page.banner.open = True
        self.page.update()
    
    def forms(self):
        """Responsável por criar o forms a ser alterado pelo ADM."""
        
        data: dict = self.fetch_proposal_model()
        self.text_fields = []
        
        self.new_info_button = ft.Row(
            controls=[
                ft.TextField(
                    label="Entre com o nome da nova informação ao forms...",
                    border_radius=ft.border_radius.all(20),
                    expand=True
                ),
                ft.IconButton(
                    icon=ft.icons.ADD,
                    icon_color=ft.colors.GREEN,
                    icon_size=40,
                    on_click=lambda _: self.add_info_on_forms(),
                )
            ]
        )
            
        self.text_fields.append(
            ft.TextField(
                label="Nome",
                border_radius=ft.border_radius.all(20),
                disabled=True,
            )
        )
        
        for item in data['content'].items():
            self.text_fields.append(
                ft.Row(
                    controls=[
                        ft.TextField(
                            label=item[0],
                            border_radius=ft.border_radius.all(20),
                            disabled=True,
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_FOREVER_SHARP,
                            icon_color=ft.colors.RED,
                            icon_size=40,
                            on_click=lambda e: self.delete_info_button(e),
                        )
                    ]
                )
            )
        
        self.save_button = ft.ElevatedButton(
            text="Salvar",
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            on_click=lambda _: self.send_forms(),
        )

        self.forms_column = ft.Column(
            controls=[self.new_info_button] + self.text_fields + [self.save_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
 
        return self.forms_column
    
    def delete_info_button(self, e):
        """Deletar informação do forms de proposta."""

        for control in self.forms_column.controls: 
            if isinstance(control, ft.Row):
                if control.controls[1] == e.control:
                    self.forms_column.controls.remove(control)
        self.update()
        
    def add_info_on_forms(self):
        """Adicionar informação ao forms de proposta."""

        self.forms_column.controls.insert(
            -1
            ,
            ft.Row(
                controls=[
                    ft.TextField(
                        label=self.new_info_button.controls[0].value,
                        border_radius=ft.border_radius.all(20),
                        disabled=True,
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER_SHARP,
                        icon_color=ft.colors.RED,
                        icon_size=40,
                        on_click=lambda e: self.delete_info_button(e),
                    )
                ]
            )
        )
        self.new_info_button.controls[0].value = ""
        self.update()

    def build(self):

        return ft.Column(
            controls=[
                ft.Divider(),
                ft.Text(
                   value="Editar Forms de Proposta",
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