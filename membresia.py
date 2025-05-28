import flet as ft
import mysql.connector
from datetime import datetime



def vista_membresias(page):
    def conectar_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Toti#landia$7",
            database="dbcity_club"
        )
    input_bg_color = "#E596CC"

    def open_picker(picker):
        picker.open = True
        page.dialog = picker
        page.update()

    # Controles
    titulo = ft.Text("Membresías", size=24, weight=ft.FontWeight.BOLD)

    txt_codigo = ft.TextField(label="Código", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)

    fecha_activacion = ft.TextField(label="Fecha de Activación", read_only=True, width=300)
    dp_activacion = ft.DatePicker(
        on_change=lambda e: (
            setattr(fecha_activacion, "value", datetime.strftime(e.control.value, "%d/%m/%Y")),
            fecha_activacion.update()
        )
    )

    fecha_vigencia = ft.TextField(label="Fecha de Vigencia", read_only=True, width=300)
    dp_vigencia = ft.DatePicker(
        on_change=lambda e: (
            setattr(fecha_vigencia, "value", datetime.strftime(e.control.value, "%d/%m/%Y")),
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

    tipo_membresia = ft.Dropdown(
        label="Tipo de Membresía",
        width=300,
        options=[
            ft.dropdown.Option("Clasica"),
            ft.dropdown.Option("Premia")
        ]
    )

    id_codigo_cliente = ft.TextField(label="ID Cliente", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")

    # --- FUNCIONES ---

    def validar_campos():
        if not all([txt_codigo.value, txt_nombre.value, fecha_activacion.value, fecha_vigencia.value, tipo_membresia.value, id_codigo_cliente.value]):
            mensaje.value = "Todos los campos deben estar completos."
            mensaje.color = "red"
            page.update()
            return False
        if not txt_codigo.value.isdigit() or not id_codigo_cliente.value.isdigit():
            mensaje.value = "Código e ID Cliente deben ser números enteros."
            mensaje.color = "red"
            page.update()
            return False
        return True

    def parsear_fecha(fecha_str):
        return datetime.strptime(fecha_str, "%d/%m/%Y").date()

    def agregar(e):
        if not validar_campos():
            return
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO membresia (codigo, nombre_Credencial, fecha_activacion, fecha_vigencia, tipo_membresia, idCliente)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                txt_codigo.value,
                txt_nombre.value,
                parsear_fecha(fecha_activacion.value),
                parsear_fecha(fecha_vigencia.value),
                tipo_membresia.value,
                id_codigo_cliente.value
            )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Membresía agregada correctamente."
            mensaje.color = "green"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            page.update()
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Fecha Activación")),
            ft.DataColumn(ft.Text("Fecha Vigencia")),
            ft.DataColumn(ft.Text("Tipo Membresía")),
            ft.DataColumn(ft.Text("ID Cliente"))
        ],
        rows=[],
        border=ft.border.all(1, "black"),
        data_row_min_height=40,
    )

    def consultar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre_Credencial, fecha_activacion, fecha_vigencia, tipo_membresia, idCliente FROM membresia")
            resultados = cursor.fetchall()
            tabla_resultado.rows.clear()

            for row in resultados:
                tabla_resultado.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row[0]))),
                            ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(row[2].strftime("%d/%m/%Y"))),
                            ft.DataCell(ft.Text(row[3].strftime("%d/%m/%Y"))),
                            ft.DataCell(ft.Text(row[4])),
                            ft.DataCell(ft.Text(str(row[5])))
                        ]
                    )
                )
            mensaje.value = f"{len(resultados)} resultados encontrados."
            mensaje.color = "green"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            page.update()
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def eliminar(e):
        if not txt_codigo.value.isdigit():
            mensaje.value = "El código debe ser un número entero."
            mensaje.color = "red"
            page.update()
            return
        codigo = int(txt_codigo.value)
        if codigo not in [int(row.cells[0].content.value) for row in tabla_resultado.rows]:
            mensaje.value = "El código no existe en la tabla."
            mensaje.color = "red"
            page.update()
            return
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM membresia WHERE codigo = %s", (codigo,))
            conn.commit()
            mensaje.value = "Membresía eliminada correctamente."
            mensaje.color = "green"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            page.update()
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def modificar(e):
        if not validar_campos():
            return
        codigo = int(txt_codigo.value)
        if codigo not in [int(row.cells[0].content.value) for row in tabla_resultado.rows]:
            mensaje.value = "El código no existe en la tabla."
            mensaje.color = "red"
            page.update()
            return
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                UPDATE membresia
                SET nombre_Credencial = %s, fecha_activacion = %s, fecha_vigencia = %s, tipo_membresia = %s, idCliente = %s
                WHERE codigo = %s
            """
            valores = (
                txt_nombre.value,
                parsear_fecha(fecha_activacion.value),
                parsear_fecha(fecha_vigencia.value),
                tipo_membresia.value,
                id_codigo_cliente.value,
                codigo
            )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Membresía modificada correctamente."
            mensaje.color = "green"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            page.update()
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    # --- Layout final ---
    fila_botones = ft.Row(
        [
            ft.ElevatedButton(text="Agregar", on_click=agregar),
            ft.ElevatedButton(text="Consultar", on_click=consultar),
            ft.ElevatedButton(text="Eliminar", on_click=eliminar),
            ft.ElevatedButton(text="Modificar", on_click=modificar),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    tabla_scrollable = ft.Column(
        controls=[tabla_resultado],
        scroll="auto",
        height=250,
        width=800
    )

 
    return ft.Column(
            [
                titulo, txt_codigo, txt_nombre, fecha_activacion, btn_fecha_activacion,
                fecha_vigencia, btn_fecha_vigencia, tipo_membresia, id_codigo_cliente,
                fila_botones, mensaje, tabla_scrollable
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll = ft.ScrollMode.ALWAYS
        )


