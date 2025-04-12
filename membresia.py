import flet as ft
import mysql.connector
from datetime import datetime

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="Toti#landia$7", 
        database="dbcity_club"        
    )

def main(page: ft.Page):
    page.title = "Catálogo de Membresías"
    page.window_width = 640
    page.window_height = 600
    page.scroll = "auto"

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_bg_color = "#E596CC"

    def open_picker(picker):
        picker.open = True
        page.dialog = picker
        page.update()

    titulo = ft.Text("Membresías", size=24, weight=ft.FontWeight.BOLD)

    txt_codigo = ft.TextField(label="Código", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)

    fecha_activacion = ft.TextField(label="Fecha de Activación", read_only=True, width=300)
    dp_activacion = ft.DatePicker(
        on_change=lambda e: (
            setattr(fecha_activacion, "value", e.control.value),
            fecha_activacion.update()
        )
    )

    fecha_vigencia = ft.TextField(label="Fecha de Vigencia", read_only=True, width=300)
    dp_vigencia = ft.DatePicker(
        on_change=lambda e: (
            setattr(fecha_vigencia, "value", e.control.value),
            fecha_vigencia.update()
        )
    )

    page.overlay.extend([dp_activacion, dp_vigencia])

    btn_fecha_activacion = ft.ElevatedButton(
        text="Seleccionar Fecha de Activación",
        on_click=lambda _: open_picker(dp_activacion)
    )
    btn_fecha_vigencia = ft.ElevatedButton(
        text="Seleccionar Fecha de Vigencia",
        on_click=lambda _: open_picker(dp_vigencia)
    )

    mensaje = ft.Text("", color="green")

    tipo_membresia = ft.Dropdown(
        label="Tipo de Membresía",
        width=300,
        options=[
            ft.dropdown.Option("Clasica"),
            ft.dropdown.Option("Premia")
        ]
    )

    def agregar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO membresia (codigo, nombre_Credencial, fecha_activacion, fecha_vigencia, tipo_membresia)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (
                txt_codigo.value,
                txt_nombre.value,
                fecha_activacion.value,
                fecha_vigencia.value,
                tipo_membresia.value
            )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Membresía agregada correctamente."
            mensaje.color = "green"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
            page.update()
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Fecha Activación")),
            ft.DataColumn(ft.Text("Fecha Vigencia")),
            ft.DataColumn(ft.Text("Tipo Membresía"))
        ],
        rows=[],
        border=ft.border.all(1, "black"),
        data_row_min_height=40,
    )

    def consultar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "SELECT codigo, nombre_Credencial, fecha_activacion, fecha_vigencia, tipo_membresia FROM membresia"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            tabla_resultado.rows.clear()

            for row in resultados:
                tabla_resultado.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row[0]))),
                            ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(datetime.strftime(row[2], "%d/%m/%Y"))),
                            ft.DataCell(ft.Text(datetime.strftime(row[3], "%d/%m/%Y"))),
                            ft.DataCell(ft.Text(row[4]))
                        ]
                    )
                )

            mensaje.value = f"{len(resultados)} resultados encontrados."
            mensaje.color = "green"
            page.update()

        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
            page.update()
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                mensaje.update()

    fila_botones = ft.Row(
        [
            ft.ElevatedButton(text="Agregar", on_click=agregar),
            ft.ElevatedButton(text="Consultar", on_click=consultar),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    tabla_scrollable = ft.Column(
        controls=[tabla_resultado],
        scroll="auto",
        height=250,
        width=640
    )

    page.add(
        ft.Column(
            [
                titulo,
                txt_codigo,
                txt_nombre,
                fecha_activacion,
                btn_fecha_activacion,
                fecha_vigencia,
                btn_fecha_vigencia,
                tipo_membresia,
                fila_botones,
                mensaje,
                tabla_scrollable
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
