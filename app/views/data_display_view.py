import flet as ft
import pandas as pd

class DataDisplayPage:
    def __init__(self, page: ft.Page, app_state):
        self.page = page
        self.app_state = app_state

    def build(self):
        df = self.app_state.get_dataframe()

        if df is None:
            return ft.Column(
                [
                    ft.Text("Visualización de Datos", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("No hay datos cargados. Por favor, carga un archivo CSV primero desde la sección 'Cargar Archivo'.")
                ]
            )

        # Información básica del DataFrame
        num_rows = len(df)
        num_cols = len(df.columns)
        headers = ", ".join(df.columns.tolist())

        # Crear la tabla de Flet para mostrar una muestra de los datos (ej. primeras 5 filas)
        data_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in df.columns],
            rows=[
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(df.iloc[i][col]))) for col in df.columns]
                ) for i in range(min(5, num_rows)) # Muestra hasta 5 filas
            ],
            # width=800, # Ajusta el ancho según necesites
            # expand=True # Si quieres que la tabla se expanda
        )
        
        # Controles para la barra superior de la maqueta ("Ver Datos", "Análisis Básico", "Análisis Avanzado")
        # Esto podría ser un ft.Tabs
        analysis_tabs = ft.Tabs(
            selected_index=0,
            # on_change=lambda e: print(f"Tab changed to: {e.control.selected_index}"),
            tabs=[
                ft.Tab(text="Vista Previa Datos"),
                ft.Tab(text="Análisis Básico"), # Aquí iría la info de filas, columnas, etc.
                ft.Tab(text="Análisis Avanzado"), # Placeholder para futuras funcionalidades
            ]
        )
        
        # Contenido para cada Tab (simplificado por ahora)
        # En una app más grande, cada tab podría cargar su propio UserControl o función de construcción
        tab_content_preview = ft.Column(
            [
                ft.Text("Vista Previa de los Datos (primeras 5 filas):", weight=ft.FontWeight.BOLD),
                ft.Container(content=data_table, border=ft.border.all(1, ft.Colors.BLACK26), border_radius=5, padding=10)
            ],
            # scroll=ft.ScrollMode.ADAPTIVE # Si la tabla es muy ancha
        )
        
        tab_content_basic_analysis = ft.Column(
            [
                ft.Text(f"Número total de filas (registros): {num_rows}"),
                ft.Text(f"Número total de columnas: {num_cols}"),
                ft.Text(f"Encabezados (nombres de columnas): {headers}"),
                # Aquí podrías añadir más análisis básicos (tipos de datos por columna, valores faltantes, etc.)
                # usando funciones de core/data_analyzer.py
            ]
        )

        tab_content_advanced_analysis = ft.Text("Funcionalidad de Análisis Avanzado (Próximamente)")

        # Contenedor para el contenido de las pestañas
        tabs_content_area = ft.Container(content=tab_content_preview) # Contenido inicial

        def handle_tab_change(e):
            selected_tab_index = e.control.selected_index
            if selected_tab_index == 0:
                tabs_content_area.content = tab_content_preview
            elif selected_tab_index == 1:
                tabs_content_area.content = tab_content_basic_analysis
            elif selected_tab_index == 2:
                tabs_content_area.content = tab_content_advanced_analysis
            self.page.update()
        
        analysis_tabs.on_change = handle_tab_change


        return ft.Column(
            [
                ft.Text("Análisis Dataset", size=24, weight=ft.FontWeight.BOLD), # Título principal de la vista
                # ft.Text(f"Dataset: {self.app_state.loaded_file_name or 'N/A'}"), # Si guardas el nombre del archivo
                analysis_tabs, # Las pestañas
                tabs_content_area, # El contenido que cambia según la pestaña
            ],
            spacing=15,
            # expand=True,
            # scroll=ft.ScrollMode.ADAPTIVE # Si el contenido es muy largo
        )

