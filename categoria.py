import flet as ft
import mysql.connector


def vista_categoria(page):
    
    def conectar_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",       
            password="Toti#landia$7", 
            database="dbcity_club"        
        )
    input_bg_color = "#E596CC"

    # Componentes
    titulo = ft.Text("Categorias", size=24, weight=ft.FontWeight.BOLD)

    txt_id_categorias = ft.TextField(label="ID Categorias", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")

    def agregar(e):
        try:
            try:
                id = int(txt_id_categorias.value)
            except ValueError:
                mensaje.value = "El id debe ser entero."
                mensaje.color = "red"
                page.update()
                return
            if id == "" or txt_nombre.value == "":
                mensaje.value = "Los campos no pueden estar vacíos."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO categoria (idCategoria, nombre)
                VALUES (%s, %s)
                """
            valores = (
                    txt_id_categorias.value,
                    txt_nombre.value,
                )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Categoria agregada correctamente."
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
            ft.DataColumn(ft.Text("ID Categoria")),
            ft.DataColumn(ft.Text("Nombre")),
        ],
        rows=[],
        width=600,
        height=200,
    )
    tabla_scroballe = ft.Column(
        [tabla_resultado],
        scroll=ft.ScrollMode.ADAPTIVE, 
        height=250, # Define una altura fija para el área visible de la tabla
        expand=True 
    )
    def consultar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "SELECT idCategoria, nombre FROM categoria"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            # Limpiar filas anteriores
            tabla_resultado.rows.clear()
            for row in resultado:
                tabla_resultado.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row[0]))),
                            ft.DataCell(ft.Text(row[1])),
                        ]))
            mensaje.value = "Consulta realizada correctamente."
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

    
    def eliminar(e):
        try:
            try:
                id = int(txt_id_categorias.value)
            except ValueError:
                mensaje.value = "El id debe ser entero."
                mensaje.color = "red"
                page.update()
                return
            if id == "":
                mensaje.value = "El id no puede estar vacío."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "DELETE FROM categoria WHERE idCategoria = %s"
            valores = (txt_id_categorias.value,)
            cursor.execute(sql, valores)
            mensaje.value = "Categoria eliminada correctamente."
            mensaje.color = "green"
            conn.commit()
            mensaje.value = "Categoria eliminada correctamente."
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
            page.update()
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
    def modificar(e):
            mensaje.color = "red"
            try:
                if txt_id_categorias.value == "" or txt_nombre.value == "":
                    mensaje.value = "Los campos no pueden estar vacíos."
                    page.update()
                    return

                try:
                    id = int(txt_id_categorias.value)
                except ValueError:
                    mensaje.value = "El id debe ser entero."
                    page.update()
                    return

                if id not in [int(row.cells[0].content.value) for row in tabla_resultado.rows]:
                    mensaje.value = "El id no existe."
                    page.update()
                    return

                conn = conectar_db()
                cursor = conn.cursor()
                sql = "UPDATE categoria SET nombre = %s WHERE idCategoria = %s"
                valores = (txt_nombre.value, id)
                cursor.execute(sql, valores)
                conn.commit()
                mensaje.value = "Categoría modificada correctamente."
                mensaje.color = "green"

            except Exception as ex:
                mensaje.value = f"Error: {str(ex)}"
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
    
    # Agregar los componentes a la interfaz
    return ft.Column(
            [
                titulo,
                txt_id_categorias,
                txt_nombre,
                fila_botones,
                mensaje,
                tabla_scroballe
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand= True
        )
