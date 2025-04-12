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
    page.title = "Catálogo de Unidad"
    page.window_width = 640
    page.window_height = 480
    page.scroll = "auto"

    # Centramos todo el contenido en la pantalla
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_bg_color = "#E596CC"

    # Componentes
    titulo = ft.Text("Unidad", size=24, weight=ft.FontWeight.BOLD)

    txt_id_unidad = ft.TextField(label="ID Unidad", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")
    def agrega_metodo(e):
        try:
            try:
                id = int(txt_id_unidad.value)
            except ValueError:
                mensaje.value = "El id debe ser entero."
                mensaje.color = "red"
                page.update()
                return

            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO unidad (idUnidad, nombre)
                VALUES (%s, %s)
                """
            valores = (
                    txt_id_unidad.value,
                    txt_nombre.value,
                )
            cursor.execute(sql, valores)
            conn.commit()

            print("Agregar unidad")
        except Exception as ex:
            mensaje.value = f" Error: {str(ex)}"
            mensaje.color = "red"
            page.update()
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Método")),
            ft.DataColumn(ft.Text("Nombre")),
        ],
        rows=[],
        border=ft.border.all(1, "black"),
        data_row_min_height=40,
    )
    def consultar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT idUnidad, nombre FROM unidad")
            resultados = cursor.fetchall()

            tabla_resultado.rows.clear()  # Limpiamos la tabla antes de llenar con nuevos datos

            for fila in resultados:
                tabla_resultado.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),
                            ft.DataCell(ft.Text(fila[1])),
                        ]
                    )
                )

            mensaje.value = f"{len(resultados)} resultados encontrados."
            mensaje.color = "green"
            page.update()

        except Exception as ex:
            mensaje.value = f"Error al consultar: {str(ex)}"
            mensaje.color = "red"
            page.update()
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()


    
    fila_botones = ft.Row(
        [
            ft.ElevatedButton(text="Agregar", on_click=agrega_metodo),
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
                txt_id_unidad,
                txt_nombre,
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