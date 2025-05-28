import flet as ft
import mysql.connector

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Toti#landia$7",
        database="dbcity_club"
    )

def vista_unidad(page):
    input_bg_color = "#E596CC"

    txt_id_unidad = ft.TextField(label="ID Unidad", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")

    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Unidad")),
            ft.DataColumn(ft.Text("Nombre")),
        ],
        rows=[],
        border=ft.border.all(1, "black"),
        data_row_min_height=40,
    )

    tabla_scrollable = ft.Column(
        [tabla_resultado],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=300,
        expand=True
    )

    def limpiar_campos():
        txt_id_unidad.value = ""
        txt_nombre.value = ""

    def agrega_metodo(e):
        try:
            id = int(txt_id_unidad.value)
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "INSERT INTO unidad (idUnidad, nombre) VALUES (%s, %s)"
            cursor.execute(sql, (id, txt_nombre.value))
            conn.commit()
            mensaje.value = "Unidad agregada correctamente."
            mensaje.color = "green"
            limpiar_campos()
        except ValueError:
            mensaje.value = "El id debe ser un número entero."
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            mensaje.update()

    def consultar(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT idUnidad, nombre FROM unidad")
            resultados = cursor.fetchall()
            tabla_resultado.rows.clear()
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
        except Exception as ex:
            mensaje.value = f"Error al consultar: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            mensaje.update()
            tabla_resultado.update()

    def eliminar(e):
        try:
            id = int(txt_id_unidad.value)
            ids_tabla = [int(row.cells[0].content.value) for row in tabla_resultado.rows]
            if id not in ids_tabla:
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                mensaje.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM unidad WHERE idUnidad = %s", (id,))
            conn.commit()
            mensaje.value = "Unidad eliminada correctamente."
            mensaje.color = "green"
            limpiar_campos()
        except ValueError:
            mensaje.value = "El id debe ser un número entero."
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error al eliminar: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            mensaje.update()

    def modificar(e):
        try:
            id = int(txt_id_unidad.value)
            if txt_nombre.value == "":
                mensaje.value = "El campo nombre no puede estar vacío."
                mensaje.color = "red"
                mensaje.update()
                return
            ids_tabla = [int(row.cells[0].content.value) for row in tabla_resultado.rows]
            if id not in ids_tabla:
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                mensaje.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE unidad SET nombre = %s WHERE idUnidad = %s", (txt_nombre.value, id))
            conn.commit()
            mensaje.value = "Unidad modificada correctamente."
            mensaje.color = "green"
            limpiar_campos()
        except ValueError:
            mensaje.value = "El id debe ser un número entero."
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error al modificar: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            mensaje.update()

    fila_botones = ft.Row(
        [
            ft.ElevatedButton(text="Agregar", on_click=agrega_metodo),
            ft.ElevatedButton(text="Consultar", on_click=consultar),
            ft.ElevatedButton(text="Eliminar", on_click=eliminar),
            ft.ElevatedButton(text="Modificar", on_click=modificar),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    return ft.Column(
        [
            ft.Text("Gestión de Unidades", size=24, weight=ft.FontWeight.BOLD),
            txt_id_unidad,
            txt_nombre,
            fila_botones,
            mensaje,
            tabla_scrollable,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
