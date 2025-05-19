import flet as ft
# import pandas as pd # Si necesitas manipular el resultado de la consulta
# from core.query_engine import execute_query_on_dataframe # Asumiendo que tendrás esto

class QueryPage:
    def __init__(self, page: ft.Page, app_state):
        self.page = page
        self.app_state = app_state
        self.query_input = ft.TextField(
            label="Escribe tu consulta SQL aquí...", 
            multiline=True, 
            min_lines=3, 
            max_lines=5,
            # expand=True
        )
        self.results_table_container = ft.Container(
            ft.Text("Los resultados de la consulta aparecerán aquí."),
            # expand=True,
            # scroll=ft.ScrollMode.ADAPTIVE
        )
        self.query_status = ft.Text("")

    def handle_execute_query(self, e):
        df_original = self.app_state.get_dataframe()
        query_str = self.query_input.value

        if df_original is None:
            self.query_status.value = "Error: No hay un DataFrame cargado para consultar."
            self.query_status.color = ft.Colors.ORANGE_700
            self.results_table_container.content = ft.Text("Carga un archivo primero.")
            self.page.update()
            return

        if not query_str:
            self.query_status.value = "Error: La consulta no puede estar vacía."
            self.query_status.color = ft.Colors.RED_ACCENT_700
            self.page.update()
            return

        try:
            # Aquí llamarías a tu motor de consultas (DuckDB sobre el DataFrame de Pandas)
            # df_result = execute_query_on_dataframe(df_original, query_str) # Desde core.query_engine
            
            # --- Simulación de ejecución de consulta ---
            # En una implementación real, usarías DuckDB.
            # Por ejemplo:
            # import duckdb
            # con = duckdb.connect(database=':memory:', read_only=False)
            # con.register('my_table', df_original)
            # df_result = con.execute(query_str).fetchdf()
            # con.close()
            # Esta es una simulación muy básica:
            if "select *" in query_str.lower() and "limit" not in query_str.lower():
                 df_result = df_original.head() # Simula un SELECT * limitado
                 self.query_status.value = "Consulta simulada (SELECT * LIMIT 5) ejecutada."
            elif "error" in query_str.lower():
                raise ValueError("Error de sintaxis simulado en la consulta.")
            else:
                 # Simula un resultado vacío o un subconjunto si la consulta es más específica
                 # Esto es muy simplista, DuckDB manejaría la lógica SQL real.
                 df_result = df_original.sample(n=min(3, len(df_original))) if not df_original.empty else df_original.head(0)
                 self.query_status.value = "Consulta simulada ejecutada (resultado de muestra)."
            # --- Fin de Simulación ---


            if not df_result.empty:
                data_table = ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(col)) for col in df_result.columns],
                    rows=[
                        ft.DataRow(
                            cells=[ft.DataCell(ft.Text(str(df_result.iloc[i][col]))) for col in df_result.columns]
                        ) for i in range(len(df_result))
                    ],
                    # width=800
                )
                self.results_table_container.content = ft.Container(content=data_table, border=ft.border.all(1, ft.Colors.BLACK26), border_radius=5, padding=10)
                self.query_status.color = ft.Colors.GREEN_ACCENT_700
            else:
                self.results_table_container.content = ft.Text("La consulta no devolvió resultados.")
                self.query_status.value = "Consulta ejecutada, pero no hay resultados."
                self.query_status.color = ft.Colors.AMBER_700
        
        except Exception as ex:
            self.results_table_container.content = ft.Text(f"Error al ejecutar la consulta.")
            self.query_status.value = f"Error: {ex}"
            self.query_status.color = ft.Colors.RED_ACCENT_700
            print(f"Error en consulta: {ex}")

        self.page.update()


    def build(self):
        return ft.Column(
            [
                ft.Text("Realizar Consultas SQL", size=24, weight=ft.FontWeight.BOLD),
                self.query_input,
                ft.ElevatedButton(
                    "Ejecutar Consulta",
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=self.handle_execute_query
                ),
                self.query_status,
                ft.Divider(),
                ft.Text("Resultados:", weight=ft.FontWeight.BOLD),
                self.results_table_container,
                # Aquí podrías añadir opciones para generar gráficos a partir de los resultados
            ],
            spacing=15,
            # expand=True,
            # scroll=ft.ScrollMode.ADAPTIVE
        )
