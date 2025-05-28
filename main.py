import flet as ft
from unidad import vista_unidad
from clientes import vista_clientes
from metodo_pago import vista_pagos
from proveedor import vista_proveedor
from membresia import vista_membresias
from empleados import vista_empleado
from categoria import vista_categoria
from articulos import vista_articulos
from ventas import vista_ventas
from descventas import vista_descventas

def main(page: ft.Page):
    page.title = "Punto de Venta"
    page.window_width = 1000
    page.window_height = 600

    contenido = ft.Container(content=vista_clientes(page), expand=True)

    def cambiar_vista(e):
        if e.control.selected_index == 0:
            contenido.content = vista_clientes(page)
        elif e.control.selected_index == 1:
            contenido.content = vista_membresias(page)
        elif e.control.selected_index == 2:
            contenido.content = vista_pagos(page)
        elif e.control.selected_index == 3:
            contenido.content = vista_proveedor(page)
        elif e.control.selected_index == 4:
            contenido.content = vista_unidad(page)
        elif e.control.selected_index == 5:
            contenido.content = vista_empleado(page)
        elif e.control.selected_index == 6:
            contenido.content = vista_categoria(page)
        elif e.control.selected_index == 7:
            contenido.content = vista_articulos(page)
        elif e.control.selected_index == 8:
            contenido.content = vista_ventas(page)
        elif e.control.selected_index == 9:
            contenido.content = vista_descventas(page)
        page.update()

    menu = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Clientes"),
            ft.NavigationRailDestination(icon=ft.Icons.CARD_MEMBERSHIP, label="Membresias"),
            ft.NavigationRailDestination(icon=ft.Icons.CREDIT_CARD, label="Metodo de Pago"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON_4_OUTLINED, label="Proveedor"),
            ft.NavigationRailDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, label="Unidad"),
            ft.NavigationRailDestination(icon=ft.Icons.FACE, label="Empleado"),
            ft.NavigationRailDestination(icon=ft.Icons.CATEGORY, label="Categoria"),
            ft.NavigationRailDestination(icon=ft.Icons.LOCAL_CONVENIENCE_STORE, label="Articulos"),
            ft.NavigationRailDestination(icon=ft.Icons.POINT_OF_SALE, label="Ventas"),
            ft.NavigationRailDestination(icon=ft.Icons.RECEIPT_LONG, label="Cons. Ventas"),
        ],
        on_change=cambiar_vista,
        extended=False,  # Hace que el menú sea más compacto
        min_width=80,    # Ancho mínimo del menú
        min_extended_width=180  # Ancho cuando se expande
    )

    page.add(
        ft.Row(
            controls=[
                menu,
                ft.VerticalDivider(width=1),
                contenido
            ],
            spacing=0,  # Reduce el espacio entre elementos
            expand=True
        )
    )

ft.app(target=main)