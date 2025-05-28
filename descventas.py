import flet as ft
import mysql.connector
from datetime import datetime

def vista_descventas(page: ft.Page):
    def conectar_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Toti#landia$7",
            database="dbcity_club"
        )
    
    # --- Componentes de la UI ---
    mensaje = ft.Text("", color=ft.Colors.GREEN_500, size=16)

    # Tabla de resumen de ventas
    tabla_ventas_resumen = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Venta")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Importe Total")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Empleado")),
            ft.DataColumn(ft.Text("Método Pago")),
        ],
        rows=[],
        heading_row_color=ft.Colors.BLUE_GREY_100,
        data_row_color={"hovered": ft.Colors.BLUE_GREY_50},
    )

    # Tabla de detalle de venta
    tabla_detalle_venta = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código Artículo")),
            ft.DataColumn(ft.Text("Nombre Artículo")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Precio Unitario")),
            ft.DataColumn(ft.Text("Subtotal")),
        ],
        rows=[],
        heading_row_color=ft.Colors.LIGHT_BLUE_100,
        data_row_color={"hovered": ft.Colors.LIGHT_BLUE_50},
    )

    # Título del detalle
    titulo_detalle = ft.Text(
        "Detalle de la Venta",
        size=20,
        weight=ft.FontWeight.BOLD,
        visible=False
    )

    # Contenedores
    contenedor_tabla_ventas = ft.Container(
        content=ft.Column(
            [tabla_ventas_resumen],
            scroll=ft.ScrollMode.ADAPTIVE
        ),
        height=300,
        border=ft.border.all(1, ft.Colors.GREY_300),
        padding=10,
        border_radius=10
    )

    contenedor_tabla_detalle = ft.Container(
        content=ft.Column(
            [titulo_detalle, tabla_detalle_venta],
            scroll=ft.ScrollMode.ADAPTIVE
        ),
        height=250,
        border=ft.border.all(1, ft.Colors.GREY_300),
        padding=10,
        border_radius=10,
        visible=False
    )

    # --- Funciones de Lógica ---
    def cargar_ventas(e=None):
        try:
            conn = conectar_db()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    v.idVentas, 
                    DATE_FORMAT(v.fecha, '%d/%m/
                    %Y') as fecha_formateada,
                    v.importe, 
                    COALESCE(c.nombre, 'N/A') as cliente,
                    COALESCE(e.nombre, 'N/A') as empleado,
                    COALESCE(mp.nombre_del_pago, 'N/A') as metodo_pago
                FROM ventas v
                LEFT JOIN Cliente c ON v.idCliente = c.idCliente
                LEFT JOIN empleados e ON v.idempleados = e.idempleados
                LEFT JOIN metodo_pago mp ON v.idmetodo_pago = mp.idmetodo_pago
                ORDER BY v.fecha DESC
            """
            cursor.execute(query)
            ventas = cursor.fetchall()

            tabla_ventas_resumen.rows.clear()
            for venta in ventas:
                tabla_ventas_resumen.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(venta['idVentas']))),
                            ft.DataCell(ft.Text(venta['fecha_formateada'])),
                            ft.DataCell(ft.Text(f"${venta['importe']:.2f}")),
                            ft.DataCell(ft.Text(venta['cliente'])),
                            ft.DataCell(ft.Text(venta['empleado'])),
                            ft.DataCell(ft.Text(venta['metodo_pago'])),
                        ],
                        on_select_changed=lambda e, id=venta['idVentas']: mostrar_detalle_venta(id)
                    )
                )
            
            mensaje.value = f"Cargadas {len(ventas)} ventas"
            mensaje.color = ft.Colors.GREEN
            
        except mysql.connector.Error as err:
            mensaje.value = f"Error de base de datos: {err}"
            mensaje.color = ft.Colors.RED
        except Exception as ex:
            mensaje.value = f"Error inesperado: {str(ex)}"
            mensaje.color = ft.Colors.RED
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def mostrar_detalle_venta(id_venta):
        try:
            conn = conectar_db()
            cursor = conn.cursor(dictionary=True)
            
            # Consulta para obtener el detalle de la venta
            query = """
                SELECT 
                    d.codigo_articulo,
                    a.nombre as nombre_articulo,
                    d.cantidad,
                    a.precio as precio_unitario,
                    d.total as subtotal
                FROM descventa d
                JOIN Articulo a ON d.codigo_articulo = a.codigo_articulo
                WHERE d.idventas = %s
            """
            cursor.execute(query, (id_venta,))
            detalles = cursor.fetchall()

            tabla_detalle_venta.rows.clear()
            for detalle in detalles:
                tabla_detalle_venta.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(detalle['codigo_articulo'])),
                            ft.DataCell(ft.Text(detalle['nombre_articulo'])),
                            ft.DataCell(ft.Text(str(detalle['cantidad']))),
                            ft.DataCell(ft.Text(f"${detalle['precio_unitario']:.2f}")),
                            ft.DataCell(ft.Text(f"${detalle['subtotal']:.2f}")),
                        ]
                    )
                )
            
            # Actualizar título y mostrar sección
            titulo_detalle.value = f"Detalle de Venta ID: {id_venta}"
            titulo_detalle.visible = True
            contenedor_tabla_detalle.visible = True
            
            mensaje.value = f"Mostrando detalle de venta {id_venta}"
            mensaje.color = ft.Colors.BLUE
            
        except mysql.connector.Error as err:
            mensaje.value = f"Error al cargar detalle: {err}"
            mensaje.color = ft.Colors.RED
        except Exception as ex:
            mensaje.value = f"Error inesperado: {str(ex)}"
            mensaje.color = ft.Colors.RED
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    # Cargar datos al iniciar
    cargar_ventas()

    return ft.Column(
        [
            ft.Text("Consulta de Ventas", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            mensaje,
            contenedor_tabla_ventas,
            contenedor_tabla_detalle,
        ],
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE
    )