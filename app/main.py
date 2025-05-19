import flet as ft
from views.bar_navigation import create_navigation_rail
from views.home_view import HomePage
from views.file_upload_view import FileUploadPage
from views.data_display_view import DataDisplayPage
from views.query_view import QueryPage
from views.library_view import LibraryPage
from views.about_view import AboutPage
from views.export_pdf_view import ExportPDFPage
from views.search_view import SearchPage
from constants import (
    VIEW_HOME,
    VIEW_UPLOAD,
    VIEW_DISPLAY,
    VIEW_QUERY,
    VIEW_EXPORT,
    VIEW_LIBRARY,
    VIEW_ABOUT,
    VIEW_SEARCH,
)

class AppState:
    """
    Una clase simple para manejar el estado compartido de la aplicación.
    Por ahora, solo almacena el DataFrame cargado.
    """
    def __init__(self):
        self.df = None  # Aquí se almacenará el DataFrame de Pandas
        self.loaded_file_name = None  # Para almacenar el nombre del archivo cargado
        self.current_theme = ft.ThemeMode.LIGHT  # Tema actual

    def load_dataframe(self, dataframe, file_name=None):
        self.df = dataframe
        self.loaded_file_name = file_name
        print(f"DataFrame cargado en AppState desde {file_name}")

    def get_dataframe(self):
        return self.df

    def get_loaded_file_name(self):
        return self.loaded_file_name

    def toggle_theme(self):
        """Alterna entre tema claro y oscuro"""
        self.current_theme = (
            ft.ThemeMode.LIGHT 
            if self.current_theme == ft.ThemeMode.DARK 
            else ft.ThemeMode.DARK
        )
        return self.current_theme

def main(page: ft.Page):
    page.title = "Data Análisis App - MugenC-Data"
    page.theme_mode = ft.ThemeMode.LIGHT  # Tema inicial
    
    # Instancia del estado de la aplicación
    app_state = AppState()

    # Referencia al NavigationRail para poder controlarlo desde main
    navigation_rail_ref = ft.Ref[ft.NavigationRail]()

    # Contenedor principal para el contenido de la vista
    main_content_area = ft.Container(
        content=ft.Text("Selecciona una opción del menú"),  # Contenido inicial
        expand=True,  # Para que ocupe el espacio disponible
        padding=ft.padding.all(20),
        alignment=ft.alignment.center  # Centra el contenido vertical y horizontalmente
    )

    # Lista que mapea los índices del NavigationRail a las rutas de vista.
    # El orden debe coincidir con los destinos definidos en bar_navigation.py
    # (excluyendo el primer elemento que es el botón de tema)
    view_routes_by_index = [
        VIEW_HOME,
        VIEW_SEARCH,
        VIEW_UPLOAD,
        VIEW_EXPORT,
        VIEW_LIBRARY,
        VIEW_ABOUT,
    ]

    def change_view(selected_route):
        """
        Cambia la vista mostrada en el área de contenido principal
        basándose en la ruta seleccionada.
        """
        nonlocal main_content_area  # Para modificar la variable del alcance exterior
        print(f"Cambiando vista a: {selected_route}")

        # Instancia la vista correcta basada en la ruta y asigna su contenido
        if selected_route == VIEW_HOME:
            main_content_area.content = HomePage(page, app_state).build()
        elif selected_route == VIEW_UPLOAD:
            main_content_area.content = FileUploadPage(page, app_state).build()
        elif selected_route == VIEW_DISPLAY:
            main_content_area.content = DataDisplayPage(page, app_state).build()
        elif selected_route == VIEW_QUERY:
            main_content_area.content = QueryPage(page, app_state).build()
        elif selected_route == VIEW_LIBRARY:
            main_content_area.content = LibraryPage(page, app_state).build()
        elif selected_route == VIEW_ABOUT:
            main_content_area.content = AboutPage(page, app_state).build()
        elif selected_route == VIEW_EXPORT:
            main_content_area.content = ExportPDFPage(page, app_state).build()
        elif selected_route == VIEW_SEARCH:
            main_content_area.content = SearchPage(page, app_state).build()
        else:
            main_content_area.content = ft.Text(f"Error: Vista no encontrada para la ruta '{selected_route}'")

        page.update()

    def toggle_theme():
        """Alterna entre tema claro y oscuro"""
        page.theme_mode = app_state.toggle_theme()
        update_theme_icon()
        page.update()

    def update_theme_icon():
        """Actualiza el icono del tema en la barra de navegación"""
        if navigation_rail_ref.current:
            destinations = navigation_rail_ref.current.destinations
            if destinations is not None and len(destinations) > 0:
                if page.theme_mode == ft.ThemeMode.DARK:
                    destinations[0].icon = ft.Icons.LIGHT_MODE_OUTLINED
                    destinations[0].selected_icon = ft.Icons.LIGHT_MODE
                    destinations[0].label = "Tema claro"
                else:
                    destinations[0].icon = ft.Icons.DARK_MODE_OUTLINED
                    destinations[0].selected_icon = ft.Icons.DARK_MODE
                    destinations[0].label = "Tema oscuro"

    def toggle_navigation_rail(e):
        """
        Alterna el estado extendido del NavigationRail y ajusta el tipo de etiqueta.
        """
        current_rail = navigation_rail_ref.current
        current_rail.extended = not current_rail.extended

        # Ajusta el label_type basado en si está extendido o no
        if current_rail.extended:
            current_rail.label_type = ft.NavigationRailLabelType.ALL
            app_title_text.visible = True
        else:
            current_rail.label_type = ft.NavigationRailLabelType.NONE
            app_title_text.visible = False

        page.update()

    # Crear la barra de navegación lateral
    create_navigation_rail(
        on_change_view=change_view,
        on_toggle_theme=toggle_theme,
        view_routes_by_index=view_routes_by_index,
        rail_state=navigation_rail_ref,
    )

    # Elemento de texto para el título de la app en la barra superior
    app_title_text = ft.Text("Data Análisis App", weight=ft.FontWeight.BOLD, size=18)

    # Layout principal de la página
    main_layout = ft.Column(
        [
            # Barra superior simple con el botón de menú y título
            ft.Row(
                [
                    ft.IconButton(
                        ft.Icons.MENU,
                        on_click=toggle_navigation_rail,
                        tooltip="Alternar barra de navegación"
                    ),
                    app_title_text,
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(height=1, color=ft.Colors.BLACK26),
            # Este Row contendrá la barra de navegación y el área de contenido principal
            ft.Row(
                [
                    navigation_rail_ref.current if navigation_rail_ref.current else ft.Container(),
                    ft.VerticalDivider(width=1),
                    main_content_area,
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH
            )
        ],
        expand=True,
    )

    # Añadimos el layout principal a la página
    page.add(main_layout)

    # Establecer la vista inicial (Inicio)
    if navigation_rail_ref.current:
        navigation_rail_ref.current.selected_index = 1  # El índice 1 corresponde a "Inicio"
        change_view(VIEW_HOME)
        update_theme_icon()  # Actualizar el icono del tema al inicio

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
    # ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)     # Para ejecutar en modo web