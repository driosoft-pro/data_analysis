import flet as ft

class HomePage:
    def __init__(self, page: ft.Page, app_state):
        self.page = page
        self.app_state = app_state # Para acceder/modificar el estado global si es necesario

    def build(self):
        """
        Construye y retorna el control raíz para la vista de Inicio.
        """
        return ft.Column(
            [
                ft.Text("Bienvenido al Analizador de Datos", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Utiliza el menú de la izquierda para navegar por las funcionalidades."),
                ft.Text("Comienza cargando un archivo CSV."),
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True # Descomenta si quieres que la columna se expanda
        )