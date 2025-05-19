import flet as ft
import pandas as pd # Necesitarás pandas: pip install pandas
# Asumiendo que tendrás data_loader.py en el futuro
# from core.data_loader import load_csv_to_dataframe 

class FileUploadPage:
    def __init__(self, page: ft.Page, app_state):
        self.page = page
        self.app_state = app_state
        self.file_path_text = ft.Text("Ningún archivo seleccionado.")
        self.upload_status_text = ft.Text("")

        # FilePicker para seleccionar archivos
        self.file_picker = ft.FilePicker(on_result=self.handle_file_picker_result)
        self.page.overlay.append(self.file_picker) # Es importante añadir el FilePicker al overlay de la página

    def handle_file_picker_result(self, e: ft.FilePickerResultEvent):
        self.upload_status_text.value = "" # Limpiar estado anterior
        if e.files:
            selected_file = e.files[0]
            self.file_path_text.value = f"Archivo seleccionado: {selected_file.name}"
            
            # Aquí llamarías a tu lógica de carga de datos desde core/data_loader.py
            # Por ahora, simularemos la carga y actualización del estado
            try:
                # Simulación: df = load_csv_to_dataframe(selected_file.path)
                # Para este ejemplo, vamos a crear un DataFrame de prueba si es un CSV
                if selected_file.name.lower().endswith(".csv"):
                    # En una app real, usarías selected_file.path para leer el archivo
                    # Aquí solo es una simulación para el ejemplo
                    # df = pd.read_csv(selected_file.path) # Así sería en la realidad
                    
                    # Simulación de carga (esto no lee el archivo real en el navegador por seguridad)
                    # En Flet web, el acceso directo a rutas de archivo locales es limitado.
                    # Para web, necesitarías que el usuario suba el contenido del archivo.
                    # Para escritorio, selected_file.path funcionaría.

                    # Para este ejemplo, vamos a asumir que el archivo es válido y creamos un df dummy
                    # En un escenario real, usarías core.data_loader
                    dummy_data = {'col1': [1, 2], 'col2': ['A', 'B']}
                    df = pd.DataFrame(dummy_data)
                    
                    self.app_state.load_dataframe(df) # Actualiza el DataFrame en el estado de la app
                    self.upload_status_text.value = f"¡'{selected_file.name}' cargado exitosamente!"
                    self.upload_status_text.color = ft.Colors.GREEN_ACCENT_700
                    
                    # Opcional: Navegar a la vista de display de datos automáticamente
                    # self.page.go(VIEW_DISPLAY) # Necesitarías implementar page.go o llamar a change_view
                else:
                    self.upload_status_text.value = "Error: Por favor, selecciona un archivo CSV."
                    self.upload_status_text.color = ft.Colors.RED_ACCENT_700
                    self.app_state.load_dataframe(None) # Limpiar DataFrame si no es CSV

            except Exception as ex:
                self.upload_status_text.value = f"Error al cargar el archivo: {ex}"
                self.upload_status_text.color = ft.Colors.RED_ACCENT_700
                self.app_state.load_dataframe(None) # Limpiar DataFrame en caso de error
        else:
            self.file_path_text.value = "Carga cancelada o ningún archivo seleccionado."
            self.app_state.load_dataframe(None)
        
        self.page.update()


    def build(self):
        return ft.Column(
            [
                ft.Text("Cargar Archivo CSV", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "Seleccionar Archivo CSV",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: self.file_picker.pick_files(
                        allow_multiple=False,
                        allowed_extensions=["csv"]
                    ),
                ),
                self.file_path_text,
                self.upload_status_text,
                ft.Text("Una vez cargado, podrás ver la información básica y realizar consultas."),
                # Aquí podrías añadir un botón "Validar Archivo" como en tu maqueta
                ft.ElevatedButton(
                    "Validar Archivo",
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    on_click=self.handle_validate_file, # Necesitarás implementar esta función
                    tooltip="Valida la estructura del archivo cargado (ej. número de columnas)"
                )
            ],
            spacing=15,
            # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def handle_validate_file(self, e):
        # Lógica para validar el archivo.
        # Esto dependerá de lo que quieras validar (ej. consistencia de columnas, tipos de datos).
        # Por ahora, solo un placeholder.
        df = self.app_state.get_dataframe()
        if df is not None:
            self.upload_status_text.value = f"Validación: El archivo tiene {len(df.columns)} columnas y {len(df)} filas."
            self.upload_status_text.color = ft.Colors.BLUE_700
        else:
            self.upload_status_text.value = "No hay archivo cargado para validar."
            self.upload_status_text.color = ft.Colors.ORANGE_700
        self.page.update()

