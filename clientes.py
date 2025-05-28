import flet as ft
import mysql.connector

def vista_clientes(page):
    input_bg_color = "#E596CC"

    txt_id_cliente = ft.TextField(label="ID Cliente", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)
    txt_telefono = ft.TextField(label="Teléfono", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")

    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Cliente")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono"))
        ],
        rows=[],
        expand=True
    )
    tabla_scrollable = ft.Column(
        [tabla_resultado],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=300,
        expand=True
    )


    def conectar_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Toti#landia$7",
            database="dbcity_club"
        )

    def limpiar_campos():
        txt_id_cliente.value = ""
        txt_nombre.value = ""
        txt_telefono.value = ""

    def agregar(e):
        if txt_id_cliente.value == "" or txt_nombre.value == "" or txt_telefono.value == "":
            mensaje.value = "Los campos no pueden estar vacíos."
            mensaje.color = "red"
            page.update()
            return
        try:
            id = int(txt_id_cliente.value)
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "INSERT INTO cliente (idCliente, nombre, telefono) VALUES (%s, %s, %s)"
            valores = (id, txt_nombre.value, txt_telefono.value)
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Cliente agregado correctamente."
            mensaje.color = "green"
            limpiar_campos()
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def consultar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT idCliente, nombre, telefono FROM cliente")
            resultado = cursor.fetchall()

            tabla_resultado.rows.clear()
            for row in resultado:
                tabla_resultado.rows.append(
                    ft.DataRow(
                        cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]
                    )
                )
            mensaje.value = "Consulta realizada correctamente."
            mensaje.color = "green"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def modificar(e):
        if txt_id_cliente.value == "" or txt_nombre.value == "" or txt_telefono.value == "":
            mensaje.value = "Los campos no pueden estar vacíos."
            mensaje.color = "red"
            page.update()
            return
        try:
            id = int(txt_id_cliente.value)
            ids_tabla = [int(row.cells[0].content.value) for row in tabla_resultado.rows]
            if id not in ids_tabla:
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "UPDATE cliente SET nombre = %s, telefono = %s WHERE idCliente = %s"
            valores = (txt_nombre.value, txt_telefono.value, id)
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Cliente modificado correctamente."
            mensaje.color = "green"
            limpiar_campos()
        except ValueError:
            mensaje.value = "El id debe ser entero."
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def eliminar(e):
        if txt_id_cliente.value == "":
            mensaje.value = "El campo ID no puede estar vacío."
            mensaje.color = "red"
            page.update()
            return
        try:
            id = int(txt_id_cliente.value)
            ids_tabla = [int(row.cells[0].content.value) for row in tabla_resultado.rows]
            if id not in ids_tabla:
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "DELETE FROM cliente WHERE idCliente = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            mensaje.value = "Cliente eliminado correctamente."
            mensaje.color = "green"
            limpiar_campos()
        except ValueError:
            mensaje.value = "El id debe ser entero."
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

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

    return ft.Column(
        [
            ft.Text("Catálogo de Clientes", size=24, weight=ft.FontWeight.BOLD),
            txt_id_cliente,
            txt_nombre,
            txt_telefono,
            fila_botones,
            mensaje,
            tabla_scrollable
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
