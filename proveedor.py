import flet as ft
import mysql.connector

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="Toti#landia$7", 
        database="dbcity_club"        
    )
def main(page: ft.Page):
    page.title = "Catálogo de Proveedores"
    page.window_width = 640
    page.window_height = 480
    page.scroll = "auto"

    # Centramos todo el contenido en la pantalla
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_bg_color = "#E596CC"

    # Componentes
    titulo = ft.Text("Proveedores", size=24, weight=ft.FontWeight.BOLD)

    txt_id_proveedor = ft.TextField(label="ID Proveedor", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)
    txt_telefono = ft.TextField(label="Teléfono", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")
    
    def agregar_proveedor(e):
        try:
            try:
                id = int(txt_id_proveedor.value)
            except ValueError:
                mensaje.value = "El id debe ser entero."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO proveedor (idproveedor, nombre, telefono)
                VALUES (%s, %s, %s)
                """
            valores = (
                    txt_id_proveedor.value,
                    txt_nombre.value,
                    txt_telefono.value,
                )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Proveedor agregado correctamente."
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
            page.update()
        
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                mensaje.update()

    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Proveedor")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono")),
        ],
        rows=[],
        width=500,
        height=200,
    )
    def consultar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "SELECT idproveedor, nombre, telefono FROM proveedor"
            cursor.execute(sql)
            resultados = cursor.fetchall()

            # Limpiar filas anteriores
            tabla_resultado.rows.clear()

            # Agregar resultados a la tabla
            for row in resultados:
                tabla_resultado.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(row[0]))),
                    ft.DataCell(ft.Text(row[1])),
                    ft.DataCell(ft.Text(row[2])),
                ]))

            mensaje.value = "Consulta realizada correctamente."
            mensaje.color = "green"
            page.update()
        except Exception as ex:
            print(f"Error: {str(ex)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
    def eliminar(e):
        try:
            try:
                id = int(txt_id_proveedor.value)
            except ValueError:
                mensaje.value = "El id debe ser entero."
                mensaje.color = "red"
                page.update()
                return
            if id not in [int(row.cells[0].content.value) for row in tabla_resultado.rows] or id == "":
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "DELETE FROM proveedor WHERE idproveedor = %s"
            valores = (txt_id_proveedor.value,)
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Proveedor eliminado correctamente."
            mensaje.color = "green"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
            page.update()
    
    def modificar(e):
        try:
            try:
                id = int(txt_id_proveedor.value)
            except ValueError:
                mensaje.value = "El id debe ser entero."
                mensaje.color = "red"
                page.update()
                return
            if id not in [int(row.cells[0].content.value) for row in tabla_resultado.rows] or id == "":
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                page.update()
                return
            elif txt_nombre.value == "" or txt_telefono.value == "":
                mensaje.value = "Los campos no pueden estar vacíos."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                UPDATE proveedor
                SET nombre = %s, telefono = %s
                WHERE idproveedor = %s
            """
            valores = (
                    txt_nombre.value,
                    txt_telefono.value,
                    txt_id_proveedor.value,
                )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Proveedor modificado correctamente."
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
            ft.ElevatedButton(text="Agregar", on_click=agregar_proveedor),
            ft.ElevatedButton(text="Consultar", on_click=consultar),
            ft.ElevatedButton(text="Eliminar", on_click=eliminar),
            ft.ElevatedButton(text="Modificar", on_click=modificar),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    # Agregar los componentes a la interfaz
    page.add(
        ft.Column(
            [
                titulo,
                txt_id_proveedor,
                txt_nombre,
                txt_telefono,
                fila_botones,
                mensaje,
                tabla_resultado
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER 
        )
    )

ft.app(target=main)