import flet as ft
import requests
    

class HomeView(ft.UserControl):
    
    def fetch_proposal_model(self):
        """Responsável por colerar modelo de proposta."""
        
        response = requests.get(
            url="http://django:8000/api/proposal_model/get/1/"
        )

        return response.json()
    
    
    def send_proposal(self):

        self.text_fields[-1].text = "Enviando..."
        self.text_fields[-1].disabled = True
        self.update()
        
        text_fields = self.text_fields[:len(self.text_fields) - 1]
        
        data = {
            "name": text_fields[0].value,
            "document": {},
        }
            
        data.update({"status": "AWAITING"})
        for text_field in text_fields[1::]:
            data["document"].update({text_field.label: text_field.value})
            
        response = requests.post(
            url="http://django:8000/api/proposal/send/",
            json=data,
        )
        
        self.text_fields[-1].text = "Enviar"
        self.text_fields[-1].disabled = False
        self.update()
            
        if response.status_code == 500:
            
            self.page.banner.bgcolor=ft.colors.AMBER_100
            self.page.banner.leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40)
            self.page.banner.content=ft.Text(
                "Infelizmente você não foi aprovado no momento, tente novamente quando tiver os requsitos necessários. "
            )
            self.page.banner.open = True
            self.page.update()
            
            return
        
        self.page.banner.bgcolor=ft.colors.GREEN_100
        self.page.banner.leading=ft.Icon(ft.icons.APPROVAL, color=ft.colors.GREEN, size=40)
        self.page.banner.content=ft.Text(
            "O senhor(a), foi aprovado para crédito com a Loans For Good. Agora você passará por uma análise do nossso gerente. Logo mais entraremos em contato com você."
        )
        self.page.banner.open = True
        self.page.update()
        
    def forms(self):
        
        data: dict = self.fetch_proposal_model()
        self.text_fields = []
        
        self.text_fields.append(
            ft.TextField(
                label="Nome",
                border_radius=ft.border_radius.all(20)
            )
        )
        
        for item in data['content'].items():
            self.text_fields.append(
                ft.TextField(
                    label=item[0],
                    border_radius=ft.border_radius.all(20)
                )

            )
        
        self.text_fields.append(
            ft.ElevatedButton(
                text="Enviar",
                bgcolor=ft.colors.GREEN,
                color=ft.colors.WHITE,
                on_click=lambda _: self.send_proposal(),
            )
        )
        
        return ft.Column(
            controls=self.text_fields,
            horizontal_alignment=ft.CrossAxisAlignment.END
        )
    
    def build(self):
        
        return ft.Column(
            controls=[
                ft.Divider(),
                ft.Text(
                   value="Proposta",
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