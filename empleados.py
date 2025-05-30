import flet as ft
import mysql.connector

# Función para conectar con la base de datos
def vista_empleado(page):
    def conectar_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",       
            password="Toti#landia$7", 
            database="dbcity_club"        
        )
    input_bg_color = "#E596CC"

    # Componentes
    titulo = ft.Text("Empleados", size=24, weight=ft.FontWeight.BOLD)

    txt_id_empleado = ft.TextField(label="ID empleado", bgcolor=input_bg_color, width=300)
    txt_nombre = ft.TextField(label="Nombre", bgcolor=input_bg_color, width=300)
    txt_apellido = ft.TextField(label="Apellido", bgcolor=input_bg_color, width=300)
    txt_puesto = ft.TextField(label="Puesto", bgcolor=input_bg_color, width=300)
    txt_sueldo = ft.TextField(label="Sueldo", bgcolor=input_bg_color, width=300)
    txt_edad = ft.TextField(label="Edad", bgcolor=input_bg_color, width=300)
    txt_telefono = ft.TextField(label="Teléfono", bgcolor=input_bg_color, width=300)

    mensaje = ft.Text("", color="green")

    def agregar_empleado(e):
        try:
            # --- Validar ID ---
            try:
                id_empleado = int(txt_id_empleado.value)
            except ValueError:
                mensaje.value = "El ID empleado debe ser un número entero."
                mensaje.color = "red"
                page.update()
                return

            # --- Validar sueldo ---
            try:
                sueldo = float(txt_sueldo.value)
            except ValueError:
                mensaje.value = "El sueldo debe ser un número decimal."
                mensaje.color = "red"
                page.update()
                return

            # --- Validar edad ---
            try:
                edad = int(txt_edad.value)
            except ValueError:
                mensaje.value = "La edad debe ser un número entero."
                mensaje.color = "red"
                page.update()
                return

            # --- Conexión y guardado ---
            if id_empleado == "" or txt_nombre.value == "" or txt_apellido.value == "" or txt_puesto.value == "" or txt_sueldo.value == "" or txt_edad.value == "" or txt_telefono.value == "":
                mensaje.value = "Los campos no pueden estar vacíos."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()

            sql = """
                INSERT INTO empleados
                    (idempleados, nombre, apellido, puesto, sueldo, edad, telefono)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
            """                              # ← ahora hay 7 %s
            valores = (
                id_empleado,                 # ← dato, no widget
                txt_nombre.value,
                txt_apellido.value,
                txt_puesto.value,
                sueldo,
                edad,
                txt_telefono.value,
            )

            cursor.execute(sql, valores)
            conn.commit()

            mensaje.value = "Empleado agregado exitosamente."
            mensaje.color = "green"

            # Limpiar campos
            for campo in [
                txt_id_empleado, txt_nombre, txt_apellido,
                txt_puesto, txt_sueldo, txt_edad, txt_telefono
            ]:
                campo.value = ""
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
            ft.DataColumn(ft.Text("ID Empleado")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido")),
            ft.DataColumn(ft.Text("Puesto")),
            ft.DataColumn(ft.Text("Sueldo")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("Teléfono")),
        ],
        rows=[],
        border=ft.border.all(1, "black"),
        data_row_min_height=40,
        heading_row_height=40,
        column_spacing=20,
        expand= True
    )
    def consultar_empleados(e):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "SELECT idempleados, nombre, apellido, puesto, sueldo, edad, telefono FROM empleados"
            cursor.execute(sql)
            resultados = cursor.fetchall()

            # Limpiar filas anteriores
            tabla_resultado.rows.clear()

            for fila in resultados:
                tabla_resultado.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]), size=12)),
                            ft.DataCell(ft.Text(fila[1], size=12)),
                            ft.DataCell(ft.Text(fila[2], size=12)),
                            ft.DataCell(ft.Text(fila[3], size=12)),
                            ft.DataCell(ft.Text(str(fila[4]), size=12)),
                            ft.DataCell(ft.Text(str(fila[5]), size=12)),
                            ft.DataCell(ft.Text(fila[6], size=12)),
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

    def eliminar_empleado(e):
        try:
            try:
                id_empleado = int(txt_id_empleado.value)
            except ValueError:
                mensaje.value = "El ID empleado debe ser un número entero."
                mensaje.color = "red"
                page.update()
                return
            if id_empleado == "" or id_empleado is None or id_empleado not in [int(row.cells[0].content.value) for row in tabla_resultado.rows]:
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = "DELETE FROM empleados WHERE idempleados = %s"
            valores = (id_empleado,)
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Empleado eliminado correctamente."
            mensaje.color = "green"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
            page.update()
    
    def modificar_empleado(e):
        try:
            try:
                id_empleado = int(txt_id_empleado.value)
            except ValueError:
                mensaje.value = "El ID empleado debe ser un número entero."
                mensaje.color = "red"
                page.update()
                return
            if id_empleado == "" or id_empleado is None or id_empleado not in [int(row.cells[0].content.value) for row in tabla_resultado.rows]:
                mensaje.value = "El ID no existe en la tabla."
                mensaje.color = "red"
                page.update()
                return
            # Validar campos
            if txt_nombre.value == "" or txt_apellido.value == "" or txt_puesto.value == "" or txt_sueldo.value == "" or txt_edad.value == "" or txt_telefono.value == "":
                mensaje.value = "Los campos no pueden estar vacíos."
                mensaje.color = "red"
                page.update()
                return
            # Validar sueldo
            try:
                sueldo = float(txt_sueldo.value)
            except ValueError:
                mensaje.value = "El sueldo debe ser un número decimal."
                mensaje.color = "red"
                page.update()
                return
            # Validar edad
            try:
                edad = int(txt_edad.value)
            except ValueError:
                mensaje.value = "La edad debe ser un número entero."
                mensaje.color = "red"
                page.update()
                return
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                UPDATE empleados
                SET nombre = %s, apellido = %s, puesto = %s, sueldo = %s, edad = %s, telefono = %s
                WHERE idempleados = %s
            """
            valores = (
                txt_nombre.value,
                txt_apellido.value,
                txt_puesto.value,
                sueldo,
                edad,
                txt_telefono.value,
                id_empleado
            )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Empleado modificado correctamente."
            mensaje.color = "green"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error: {str(ex)}"
            mensaje.color = "red"
            page.update()
    
    tabla_scrollable = ft.Row(
        controls=[tabla_resultado],
        scroll="auto",
        width=850
    )

    fila_botones = ft.Row(
        [
            ft.ElevatedButton(text="Agregar", on_click=agregar_empleado),
            ft.ElevatedButton(text="Consultar", on_click=consultar_empleados),
            ft.ElevatedButton(text="Eliminar", on_click=eliminar_empleado),
            ft.ElevatedButton(text="Modificar", on_click=modificar_empleado),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    return ft.Column(
            [
                titulo,
                txt_id_empleado,
                txt_nombre,
                txt_apellido,
                txt_puesto,
                txt_sueldo,
                txt_edad,
                txt_telefono,
                fila_botones,
                mensaje,
                tabla_scrollable
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll= ft.ScrollMode.ALWAYS
        )