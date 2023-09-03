import flet as ft
import requests
from threading import Thread
from time import sleep
    

class ProposalsView(ft.UserControl):
    
    
    def fetch_proposal_data(self):
        """Responsável por colerar as propostas dos clientes da API."""

        response = requests.get(
            url="http://django:8000/api/proposal/data/",
            headers={"Authorization": f"Bearer {self.page.client_storage.get('flet_frontend.auth_token')['access']}"},
        )
        
        if response.status_code == 401:
            self.page.client_storage.remove('flet_frontend.auth_token')
            self.page.go("/")  
            return 
            
        return response.json()
    
    def send_approval_results(self, e):
        
        key = e.control.key
  
        response = requests.put(
            url=f"http://django:8000/api/proposal/data/{key['id']}/",
            headers={"Authorization": f"Bearer {self.page.client_storage.get('flet_frontend.auth_token')['access']}"},
            json=key
        )
  
        if response.status_code == 401:
            self.page.client_storage.remove('flet_frontend.auth_token')
            self.page.go("/")  
            return 
            
        for control in self.proposals:
            if control.key["id"] == key["id"]:
                if key["status"] == "REFUSED": 
                    control.bgcolor = ft.colors.RED
                elif key["status"] == "APPROVED":
                    control.bgcolor = ft.colors.GREEN
                else:
                    control.bgcolor = ft.colors.BLUE
            
        self.update()
    
    def forms(self):
        """Responsável por criar a coluna de forms."""
        
        self.returned_forms =  ft.Column(
            controls=[],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        return self.returned_forms
    
        
    def clients(self):
        """Responsável por criar a coluna de clientes."""
        
        data: dict = self.fetch_proposal_data()

        self.proposals = []
        
        self.update()

        for item in data:
            
            if item["status"] == "REFUSED": 
                bgcolor = ft.colors.RED
            elif item["status"] == "APPROVED":
                bgcolor = ft.colors.GREEN
            else:
                bgcolor = ft.colors.BLUE
  
            self.proposals.append(

                ft.ElevatedButton(
                    text=item["name"],
                    bgcolor=bgcolor,
                    color=ft.colors.WHITE,
                    key=item,
                    on_click=lambda e: self.fill_forms(e),
                    width=600
                )

            )
            
        self.proposals[0].on_click(None)

        return ft.Column(
            controls=self.proposals,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def fill_forms(self, e):
        """Responsável por preencher o forms quando o ADM clica no nome do cliente."""
        
        if e == None:
            key = self.proposals[0].key
        else:
            key = e.control.key
   
        self.returned_forms.controls = []

        self.returned_forms.controls.append(
                
                ft.TextField(
                    label="Nome",
                    value=key["name"],
                    border_radius=ft.border_radius.all(20),
                    read_only=True
                )
            )
        
        for item in key["document"].items():
    
            self.returned_forms.controls.append(
                
                ft.TextField(
                    label=item[0],
                    value=item[1],
                    border_radius=ft.border_radius.all(20),
                    read_only=True
                )
            )   
        
        self.returned_forms.controls.append(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Aprovar",
                        bgcolor=ft.colors.GREEN,
                        color=ft.colors.WHITE,
                        on_click=lambda e: self.send_approval_results(e),
                        key={"status": "APPROVED", "id": key["id"], 'name': key["name"], "document": key["document"]}
                    ),
                    ft.ElevatedButton(
                        text="Em Análise",
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        on_click=lambda e: self.send_approval_results(e),
                        key={"status": "AWAITING", "id": key["id"], 'name': key["name"], "document": key["document"]}
                    ),
                    ft.ElevatedButton(
                        text="Recusar",
                        bgcolor=ft.colors.RED,
                        color=ft.colors.WHITE,
                        on_click=lambda e: self.send_approval_results(e),
                        key={"status": "REFUSED", "id": key["id"], 'name': key["name"], "document": key["document"]}
                    ),

                ],
                alignment=ft.MainAxisAlignment.END
            )
        )
        
        self.update()
            

    def thread(self):
        """Thread para iniciar coluna de clientes um pouco depois, para previnir erro no flet."""
        
        sleep(0.1)
    
        self.returned_column.controls[2].controls[0].content = self.clients()
        self.update()
        
    def build(self):
        
        self.returned_column = ft.Column(
            controls=[
                ft.Divider(),
                ft.Text(
                   value="Propostas Aguardando Análise",
                   weight=ft.FontWeight.BOLD,
                   size=30
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=None,
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
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        Thread(target=self.thread).start()
        
        return self.returned_column