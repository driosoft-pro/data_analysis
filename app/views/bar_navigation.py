import flet as ft
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

def create_navigation_rail(on_change_view, on_toggle_theme, view_routes_by_index, rail_state):
    """
    Crea y retorna el control ft.NavigationRail para la barra lateral,
    con funcionalidad de colapsar/expandir y cambio de tema.

    Args:
        on_change_view (function): Función para cambiar de vista.
        on_toggle_theme (function): Función para alternar el tema.
        view_routes_by_index (list): Lista de rutas correspondientes a los destinos de vista.
        rail_state (ft.Ref): Referencia al NavigationRail para controlar su estado.
    """

    # Definición de los destinos de navegación
    # El orden aquí DEBE coincidir con el orden en view_routes_by_index
    destinations = [
        ft.NavigationRailDestination(
            icon=ft.Icons.DARK_MODE_OUTLINED,
            selected_icon=ft.Icons.DARK_MODE,
            label="Tema",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.HOME_OUTLINED,
            selected_icon=ft.Icons.HOME,
            label="Inicio",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.SEARCH_OUTLINED,
            selected_icon=ft.Icons.SEARCH,
            label="Buscar",
        ), 
        ft.NavigationRailDestination(
            icon=ft.Icons.FOLDER_OPEN_OUTLINED,
            selected_icon=ft.Icons.FOLDER_OPEN,
            label="Cargar Archivo",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
            selected_icon=ft.Icons.PICTURE_AS_PDF,
            label="Exportar PDF",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.BOOK_OUTLINED,
            selected_icon=ft.Icons.BOOK,
            label="Library",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.INFO_OUTLINE,
            selected_icon=ft.Icons.INFO,
            label="Acerca De",
        ),
    ]

    def handle_rail_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            # Índice 0 es el botón de tema
            on_toggle_theme()
            # Restablecemos la selección para que no quede marcado
            e.control.selected_index = None
        elif 0 < selected_index <= len(view_routes_by_index):
            # Ajustamos el índice porque el primer elemento es el botón de tema
            route_to_load = view_routes_by_index[selected_index - 1]
            on_change_view(route_to_load)
        else:
            print(f"Índice fuera de rango: {selected_index}")

    rail_state.current = ft.NavigationRail(
        selected_index=None,  # Inicia sin selección
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=70,
        min_extended_width=200,
        extended=True,
        group_alignment=-0.9,
        destinations=destinations,
        on_change=handle_rail_change,
    )

    return rail_state.current