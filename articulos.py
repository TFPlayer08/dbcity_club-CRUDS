import flet as ft
import mysql.connector

def vista_articulos(page):
    def conectar_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Toti#landia$7",
            database="dbcity_club"
        )
    
    input_bg_color = "#E596CC"

    # Input fields
    codigo_articulo = ft.TextField(label="Código Artículo", bgcolor=input_bg_color, width=300)
    nombre_articulo = ft.TextField(label="Nombre Artículo", bgcolor=input_bg_color, width=300)
    precio = ft.TextField(label="Precio", bgcolor=input_bg_color, width=300)
    costo = ft.TextField(label="Costo", bgcolor=input_bg_color, width=300)
    existencia = ft.TextField(label="Existencia", bgcolor=input_bg_color, width=300)
    idCategoria = ft.TextField(label="ID Categoría", bgcolor=input_bg_color, width=300)
    idProveedor = ft.TextField(label="ID Proveedor", bgcolor=input_bg_color, width=300)
    idUnidad = ft.TextField(label="ID Unidad", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")

    # Table configuration
    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Costo")),
            ft.DataColumn(ft.Text("Existencia")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Proveedor")),
            ft.DataColumn(ft.Text("Unidad"))
        ],
        rows=[],
        expand=True,
    )
    
    tabla_scroll = ft.Column(
        [tabla_resultado],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=400,
        expand=True
    )

    def limpiar_campos():
        codigo_articulo.value = ""
        nombre_articulo.value = ""
        precio.value = ""
        costo.value = ""
        existencia.value = ""
        idCategoria.value = ""
        idProveedor.value = ""
        idUnidad.value = ""
        page.update()

    def limpiar_tabla():
        tabla_resultado.rows.clear()
        page.update()

    def buscar_articulo(e):
        if not codigo_articulo.value:
            mensaje.value = "Debe ingresar un código de artículo para buscar."
            mensaje.color = "red"
            page.update()
            return
            
        conn = None
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT codigo_articulo, nombre, precio, costo, existencia, idCategoria, idProveedor, idUnidad 
                FROM articulo 
                WHERE codigo_articulo = %s
            """, (codigo_articulo.value,))
            
            resultado = cursor.fetchone()
            limpiar_tabla()
            
            if resultado:
                celdas = [
                    ft.DataCell(ft.Text(str(resultado[0]))),
                    ft.DataCell(ft.Text(str(resultado[1]))),
                    ft.DataCell(ft.Text(str(resultado[2]))),
                    ft.DataCell(ft.Text(str(resultado[3]))),
                    ft.DataCell(ft.Text(str(resultado[4]))),
                    ft.DataCell(ft.Text(str(resultado[5]))),
                    ft.DataCell(ft.Text(str(resultado[6]))),
                    ft.DataCell(ft.Text(str(resultado[7])))
                ]
                
                tabla_resultado.rows.append(ft.DataRow(cells=celdas))
                
                nombre_articulo.value = str(resultado[1])
                precio.value = str(resultado[2])
                costo.value = str(resultado[3])
                existencia.value = str(resultado[4])
                idCategoria.value = str(resultado[5])
                idProveedor.value = str(resultado[6])
                idUnidad.value = str(resultado[7])
                
                mensaje.value = "Artículo encontrado."
                mensaje.color = "green"
            else:
                mensaje.value = "No se encontró ningún artículo con ese código."
                mensaje.color = "red"
                limpiar_campos()
                
        except mysql.connector.Error as err:
            mensaje.value = f"Error de base de datos: {err}"
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error inesperado: {str(ex)}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def agregar_articulo(e):
        if not all([codigo_articulo.value, nombre_articulo.value, precio.value, costo.value,
                    existencia.value, idCategoria.value, idProveedor.value, idUnidad.value]):
            mensaje.value = "Todos los campos son obligatorios."
            mensaje.color = "red"
            page.update()
            return

        try:
            precio_value = float(precio.value)
            costo_value = float(costo.value)
            existencia_value = int(existencia.value)
            id_categoria_value = int(idCategoria.value)
            id_proveedor_value = int(idProveedor.value)
            id_unidad_value = int(idUnidad.value)
        except ValueError:
            mensaje.value = "Los campos Precio, Costo, Existencia, ID Categoría, ID Proveedor y ID Unidad deben ser numéricos."
            mensaje.color = "red"
            page.update()
            return
            
        conn = None
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM articulo WHERE codigo_articulo = %s", (codigo_articulo.value,))
            if cursor.fetchone()[0] > 0:
                mensaje.value = "Ya existe un artículo con ese código."
                mensaje.color = "red"
                page.update()
                return
            
            sql = """
                INSERT INTO articulo (codigo_articulo, nombre, precio, costo, existencia, idCategoria, idProveedor, idUnidad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                codigo_articulo.value,
                nombre_articulo.value,
                precio_value,
                costo_value,
                existencia_value,
                id_categoria_value,
                id_proveedor_value,
                id_unidad_value
            )
            cursor.execute(sql, valores)
            conn.commit()
            mensaje.value = "Artículo agregado correctamente."
            mensaje.color = "green"
            limpiar_campos()
            consultar_articulos(None)
        except mysql.connector.Error as err:
            mensaje.value = f"Error de base de datos: {err}"
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error inesperado: {str(ex)}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def eliminar_articulo(e):
        if not codigo_articulo.value:
            mensaje.value = "El campo Código Artículo no puede estar vacío."
            mensaje.color = "red"
            page.update()
            return
            
        conn = None
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM articulo WHERE codigo_articulo = %s", (codigo_articulo.value,))
            if cursor.fetchone()[0] == 0:
                mensaje.value = "El Código Artículo no existe."
                mensaje.color = "red"
                page.update()
                return

            sql = "DELETE FROM articulo WHERE codigo_articulo = %s"
            cursor.execute(sql, (codigo_articulo.value,))
            conn.commit()
            mensaje.value = "Artículo eliminado correctamente."
            mensaje.color = "green"
            limpiar_campos()
            limpiar_tabla()
        except mysql.connector.Error as err:
            mensaje.value = f"Error de base de datos: {err}"
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error inesperado: {str(ex)}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def modificar_articulo(e):
        if not codigo_articulo.value:
            mensaje.value = "El campo Código Artículo es obligatorio para modificar."
            mensaje.color = "red"
            page.update()
            return
            
        if not any([nombre_articulo.value, precio.value, costo.value, 
                   existencia.value, idCategoria.value, idProveedor.value, idUnidad.value]):
            mensaje.value = "Debe proporcionar al menos un campo adicional a modificar."
            mensaje.color = "red"
            page.update()
            return
            
        conn = None
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM articulo WHERE codigo_articulo = %s", (codigo_articulo.value,))
            if cursor.fetchone()[0] == 0:
                mensaje.value = "El artículo no existe."
                mensaje.color = "red"
                page.update()
                return
                
            sql = "UPDATE articulo SET "
            parametros = []
            campos_actualizados = []
            
            if nombre_articulo.value:
                campos_actualizados.append("nombre = %s")
                parametros.append(nombre_articulo.value)
                
            if precio.value:
                try:
                    precio_value = float(precio.value)
                    campos_actualizados.append("precio = %s")
                    parametros.append(precio_value)
                except ValueError:
                    mensaje.value = "El precio debe ser un número válido."
                    mensaje.color = "red"
                    page.update()
                    return
                    
            if costo.value:
                try:
                    costo_value = float(costo.value)
                    campos_actualizados.append("costo = %s")
                    parametros.append(costo_value)
                except ValueError:
                    mensaje.value = "El costo debe ser un número válido."
                    mensaje.color = "red"
                    page.update()
                    return
                    
            if existencia.value:
                try:
                    existencia_value = int(existencia.value)
                    campos_actualizados.append("existencia = %s")
                    parametros.append(existencia_value)
                except ValueError:
                    mensaje.value = "La existencia debe ser un número entero válido."
                    mensaje.color = "red"
                    page.update()
                    return
                    
            if idCategoria.value:
                try:
                    id_categoria_value = int(idCategoria.value)
                    campos_actualizados.append("idCategoria = %s")
                    parametros.append(id_categoria_value)
                except ValueError:
                    mensaje.value = "El ID Categoría debe ser un número entero válido."
                    mensaje.color = "red"
                    page.update()
                    return
                    
            if idProveedor.value:
                try:
                    id_proveedor_value = int(idProveedor.value)
                    campos_actualizados.append("idProveedor = %s")
                    parametros.append(id_proveedor_value)
                except ValueError:
                    mensaje.value = "El ID Proveedor debe ser un número entero válido."
                    mensaje.color = "red"
                    page.update()
                    return
                    
            if idUnidad.value:
                try:
                    id_unidad_value = int(idUnidad.value)
                    campos_actualizados.append("idUnidad = %s")
                    parametros.append(id_unidad_value)
                except ValueError:
                    mensaje.value = "El ID Unidad debe ser un número entero válido."
                    mensaje.color = "red"
                    page.update()
                    return
            
            sql += ", ".join(campos_actualizados)
            sql += " WHERE codigo_articulo = %s"
            parametros.append(codigo_articulo.value)
            
            cursor.execute(sql, tuple(parametros))
            conn.commit()
            
            mensaje.value = "Artículo modificado correctamente."
            mensaje.color = "green"
            buscar_articulo(e)
        except mysql.connector.Error as err:
            mensaje.value = f"Error de base de datos: {err}"
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error inesperado: {str(ex)}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def consultar_articulos(e):
        conn = None
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT codigo_articulo, nombre, precio, costo, existencia, idCategoria, idProveedor, idUnidad 
                FROM articulo
            """)
            resultados = cursor.fetchall()
            
            limpiar_tabla()
            
            for resultado in resultados:
                celdas = [
                    ft.DataCell(ft.Text(str(resultado[0]))),
                    ft.DataCell(ft.Text(str(resultado[1]))),
                    ft.DataCell(ft.Text(str(resultado[2]))),
                    ft.DataCell(ft.Text(str(resultado[3]))),
                    ft.DataCell(ft.Text(str(resultado[4]))),
                    ft.DataCell(ft.Text(str(resultado[5]))),
                    ft.DataCell(ft.Text(str(resultado[6]))),
                    ft.DataCell(ft.Text(str(resultado[7])))
                ]
                tabla_resultado.rows.append(ft.DataRow(cells=celdas))
            
            mensaje.value = f"Se encontraron {len(resultados)} artículos."
            mensaje.color = "green"
        except mysql.connector.Error as err:
            mensaje.value = f"Error de base de datos al consultar: {err}"
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error inesperado al consultar: {str(ex)}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    # Button row
    fila_botones = ft.Row(
        [
            ft.ElevatedButton("Agregar", on_click=agregar_articulo),
            ft.ElevatedButton("Eliminar", on_click=eliminar_articulo),
            ft.ElevatedButton("Modificar", on_click=modificar_articulo),
            ft.ElevatedButton("Buscar", on_click=buscar_articulo),
            ft.ElevatedButton("Consultar Todos", on_click=consultar_articulos)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    return ft.Column(
        [
            ft.Text("Catálogo de Artículos", size=24, weight=ft.FontWeight.BOLD),
            codigo_articulo,
            nombre_articulo,
            precio,
            costo,
            existencia,
            idCategoria,
            idProveedor,
            idUnidad,
            fila_botones,
            mensaje,
            tabla_scroll,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.ALWAYS
    )