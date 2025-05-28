import flet as ft
import mysql.connector

def vista_pagos(page):
    def conectar_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",       
            password="Toti#landia$7", 
            database="dbcity_club"        
        )
    
    input_bg_color = "#E596CC"
    txt_id_metodopago = ft.TextField(label="ID Método de pago", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")

    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Método")),
            ft.DataColumn(ft.Text("Nombre")),
        ],
        rows=[],
        border=ft.border.all(1, "black"),
        data_row_min_height=40,
    )

    def agrega_metodo(e):
        try:
            id = int(txt_id_metodopago.value)
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO metodo_pago (idmetodo_pago, nombre_del_pago)
                VALUES (%s, %s)
            """
            valores = (txt_id_metodopago.value, txt_nombre.value)
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Método de pago agregado correctamente."
            mensaje.color = "green"
        except ValueError:
            mensaje.value = "El ID debe ser entero."
            mensaje.color = "red"
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
            cursor.execute("SELECT idmetodo_pago, nombre_del_pago FROM metodo_pago")
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
            page.update()

    def eliminar(e):
        try:
            id = int(txt_id_metodopago.value)
            ids = [int(row.cells[0].content.value) for row in tabla_resultado.rows]
            if id not in ids:
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM metodo_pago WHERE idmetodo_pago = %s", (id,))
            conn.commit()
            mensaje.value = "Método de pago eliminado correctamente."
            mensaje.color = "green"
        except ValueError:
            mensaje.value = "El ID debe ser entero."
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def modificar(e):
        if txt_id_metodopago.value == "" or txt_nombre.value == "":
            mensaje.value = "Los campos no pueden estar vacíos."
            mensaje.color = "red"
            page.update()
            return
        try:
            id = int(txt_id_metodopago.value)
            ids = [int(row.cells[0].content.value) for row in tabla_resultado.rows]
            if id not in ids:
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE metodo_pago SET nombre_del_pago = %s WHERE idmetodo_pago = %s",
                (txt_nombre.value, id)
            )
            conn.commit()
            mensaje.value = "Método de pago modificado correctamente."
            mensaje.color = "green"
        except ValueError:
            mensaje.value = "El ID debe ser entero."
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
            ft.ElevatedButton(text="Agregar", on_click=agrega_metodo),
            ft.ElevatedButton(text="Consultar", on_click=consultar),
            ft.ElevatedButton(text="Eliminar", on_click=eliminar),
            ft.ElevatedButton(text="Modificar", on_click=modificar),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    return ft.Column(
        [
            ft.Text("Métodos de Pago", size=24, weight=ft.FontWeight.BOLD),
            txt_id_metodopago,
            txt_nombre,
            fila_botones,
            mensaje,
            tabla_resultado
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
