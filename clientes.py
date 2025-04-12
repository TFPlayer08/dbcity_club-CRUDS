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
    page.title = "Catálogo de Clientes"
    page.window_width = 640
    page.window_height = 480
    page.scroll = "auto"

    # Centramos todo el contenido en la pantalla
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_bg_color = "#E596CC"

    # Componentes
    titulo = ft.Text("Clientes", size=24, weight=ft.FontWeight.BOLD)

    txt_id_cliente = ft.TextField(label="ID Cliente", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)
    txt_telefono = ft.TextField(label="Teléfono", bgcolor=input_bg_color, width=300)
    txt_codigo = ft.TextField(label="Código", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")

    def agregar(e):
        try:
            try:
                id = int(txt_id_cliente.value)
            except ValueError:
                mensaje.value = "El id debe ser entero."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO cliente (idCliente, nombre, telefono, codigo)
                VALUES (%s, %s, %s, %s)
                """
            valores = (
                    txt_id_cliente.value,
                    txt_nombre.value,
                    txt_telefono.value,
                    txt_codigo.value,
                )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Cliente agregado correctamente."
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
            ft.DataColumn(ft.Text("ID Cliente")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Código")),
        ],
        rows=[],
    )
    def consultar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "SELECT idCliente, nombre, telefono, codigo FROM cliente"
            cursor.execute(sql)
            resultado = cursor.fetchall()

            # Limpiar filas anteriores
            tabla_resultado.rows.clear()

            # Agregar nuevas filas
            for row in resultado:
                tabla_resultado.rows.append(
                    ft.DataRow(
                        cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]
                    )
                )

            mensaje.value = "Consulta realizada correctamente."
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                tabla_resultado.update()
                mensaje.update()
    
    
    fila_botones = ft.Row(
        [
            ft.ElevatedButton(text="Agregar", on_click=agregar),
            ft.ElevatedButton(text="Consultar", on_click=consultar),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    # Agregar los componentes a la interfaz
    page.add(
        ft.Column(
            [
                titulo,
                txt_id_cliente,
                txt_nombre,
                txt_telefono,
                txt_codigo,
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
