import flet as ft
import pandas as pd

class SearchPage:
    """
    Vista para la sección de Búsqueda dentro del DataFrame cargado.
    """
    def __init__(self, page: ft.Page, app_state):
        self.page = page
        self.app_state = app_state # Acceso al estado de la app para obtener datos
        self.search_input = ft.TextField(
            label="Introduce el texto a buscar...",
            # expand=True # Puedes descomentar si quieres que ocupe más espacio horizontal
        )
        # Podrías añadir un Dropdown o Checkboxes para seleccionar columnas
        # Por ahora, buscaremos en todas las columnas de tipo string.
        self.results_table_container = ft.Container(
            ft.Text("Los resultados de la búsqueda aparecerán aquí."),
            # expand=True, # Para que ocupe el espacio disponible
            # scroll=ft.ScrollMode.ADAPTIVE # Si los resultados son muchos
        )
        self.search_status = ft.Text("")

    def handle_search(self, e):
        """
        Maneja el evento de clic del botón de búsqueda.
        Realiza la búsqueda en el DataFrame cargado.
        """
        df = self.app_state.get_dataframe()
        search_text = (self.search_input.value or "").strip()

        if df is None:
            self.search_status.value = "Error: No hay un DataFrame cargado para buscar."
            self.search_status.color = ft.Colors.ORANGE_700
            self.results_table_container.content = ft.Text("Carga un archivo primero.")
            self.page.update()
            return

        if not search_text:
            self.search_status.value = "Error: El texto de búsqueda no puede estar vacío."
            self.search_status.color = ft.Colors.RED_ACCENT_700
            self.results_table_container.content = ft.Text("Introduce un texto para buscar.")
            self.page.update()
            return

        try:
            # --- Lógica de Búsqueda ---
            # Buscar el texto en todas las columnas de tipo objeto (generalmente strings)
            # Puedes adaptar esto para buscar en tipos numéricos o seleccionar columnas específicas.

            # Identificar columnas de tipo objeto (strings)
            string_columns = df.select_dtypes(include='object').columns

            if string_columns.empty:
                self.search_status.value = "No hay columnas de texto para buscar en este DataFrame."
                self.search_status.color = ft.Colors.AMBER_700
                self.results_table_container.content = ft.Text("DataFrame no contiene columnas de texto.")
                self.page.update()
                return

            # Crear una máscara booleana: True si alguna columna contiene el texto
            # Usamos .astype(str) para asegurar que todos los valores sean strings antes de .str.contains
            mask = df[string_columns].astype(str).apply(
                lambda col: col.str.contains(search_text, case=False, na=False) # case=False para búsqueda insensible a mayúsculas/minúsculas
            ).any(axis=1) # any(axis=1) busca si CUALQUIER columna en esa fila contiene el texto

            # Filtrar el DataFrame usando la máscara
            df_results = df[mask]

            # --- Mostrar Resultados ---
            if not df_results.empty:
                data_table = ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(col)) for col in df_results.columns],
                    rows=[
                        ft.DataRow(
                            cells=[ft.DataCell(ft.Text(str(df_results.iloc[i][col]))) for col in df_results.columns]
                        ) for i in range(len(df_results)) # Muestra todas las filas encontradas
                    ],
                    # width=800 # Ajusta si es necesario
                )
                self.results_table_container.content = ft.Container(content=data_table, border=ft.border.all(1, ft.Colors.BLACK26), border_radius=5, padding=10)
                self.search_status.value = f"Se encontraron {len(df_results)} resultados."
                self.search_status.color = ft.Colors.GREEN_ACCENT_700
            else:
                self.results_table_container.content = ft.Text(f"No se encontraron resultados para '{search_text}'.")
                self.search_status.value = "Búsqueda completada, no se encontraron resultados."
                self.search_status.color = ft.Colors.AMBER_700

        except Exception as ex:
            self.results_table_container.content = ft.Text(f"Error al realizar la búsqueda.")
            self.search_status.value = f"Error: {ex}"
            self.search_status.color = ft.Colors.RED_ACCENT_700
            print(f"Error en búsqueda: {ex}")

        self.page.update()


    def build(self):
        """
        Construye y retorna el control raíz para la vista de Búsqueda.
        """
        return ft.Column(
            [
                ft.Text("Buscar en Datos en el DataFrame cargado.", size=18, weight=ft.FontWeight.BOLD),
                self.search_input,
                ft.ElevatedButton(
                    "Buscar",
                    icon=ft.Icons.SEARCH,
                    on_click=self.handle_search
                ),
                self.search_status,
                ft.Divider(),
                ft.Text("Resultados de la Búsqueda:", weight=ft.FontWeight.BOLD),
                self.results_table_container,
            ],
            spacing=15,
        )