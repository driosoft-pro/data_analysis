import flet as ft

class AboutPage:
    """
    Vista para la sección "Acerca De".
    """
    def __init__(self, page: ft.Page, app_state):
        self.page = page
        self.app_state = app_state # Acceso al estado de la app si es necesario

    def build(self):
        """
        Construye y retorna el control raíz para la vista de Acerca De.
        """
        return ft.Column(
            [
                ft.Text("Acerca De", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Esta es una aplicación de análisis de datos construida con Flet."),
                ft.Text("Desarrollado por Driosoft-Pro."),
                ft.Text("Versión: 1.0.0"),
                ft.Text("Para más información, visita https://github.com/driosoft-pro/data_analysis.git."),
            ],
            spacing=15,
        )
