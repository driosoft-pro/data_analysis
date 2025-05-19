import flet as ft
import pandas as pd

class LibraryPage:
    """
    Vista para mostrar información sobre la "Biblioteca" o librerías usadas.
    """
    def __init__(self, page: ft.Page, app_state):
        self.page = page
        self.app_state = app_state # Acceso al estado de la app si es necesario

    def build(self):
        """
        Construye y retorna el control raíz para la vista de Biblioteca.
        """
        # Aquí puedes mostrar información sobre las librerías de Python usadas
        # o quizás una lista de datasets cargados previamente si esa es la idea de "Library"
        
        libraries_info = [
            "Flet: Para la interfaz de usuario.",
            "Flet-desktop: Soporte para empaquetar como aplicación de escritorio.",
            "Flet-webview: Integración con WebView (si se usa).",
            "Pandas: Para manipulación y análisis de datos.",
            "DuckDB: Para consultas SQL sobre DataFrames.",
            "ReportLab: Para generación de PDFs.",
            "NumPy: Para cálculos numéricos avanzados.",
            "Matplotlib: Para visualización de datos.",
            "Seaborn: Para visualización estadística.",
            "scipy: Para cálculos numéricos avanzados.",
            "tabulate: Para tablas en formato texto (para consola, si se desea).",
            "black: Formateador automático.",
            "flake8: Verificación de estilo de código.",
            "isort: Ordenamiento automático de imports.",
            "pytest: Testing unitario y de integración.",
            "PyInstaller: Para crear ejecutables de escritorio.",
        ]

        libraries_list = ft.Column([ft.Text(f"- {lib}") for lib in libraries_info])

        return ft.Column(
            [
                ft.Text("Librerías Utilizadas", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Esta aplicación utiliza las siguientes librerías principales:"),
                libraries_list,
                ft.Text("\n(Nota: El contenido de esta sección puede variar según la version de la aplicación)"),
            ],
            spacing=15,
            # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )