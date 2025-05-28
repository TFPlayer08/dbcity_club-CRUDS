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

    codigo_articulo = ft.TextField(label="Código Artículo", bgcolor=input_bg_color, width=300)
    nombre_articulo = ft.TextField(label="Nombre Artículo", bgcolor=input_bg_color, width=300)
    precio = ft.TextField(label="Precio", bgcolor=input_bg_color, width=300)
    costo = ft.TextField(label="Costo", bgcolor=input_bg_color, width=300)
    existencia = ft.TextField(label="Existencia", bgcolor=input_bg_color, width=300)
    idCategoria = ft.TextField(label="ID Categoría", bgcolor=input_bg_color, width=300)
    idProveedor = ft.TextField(label="ID Proveedor", bgcolor=input_bg_color, width=300)
    idUnidad = ft.TextField(label="ID Unidad", bgcolor=input_bg_color, width=300)
    mensaje = ft.Text("", color="green")

    tabla_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código Artículo")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Costo")),
            ft.DataColumn(ft.Text("Existencia")),
            ft.DataColumn(ft.Text("ID Categoría")),
            ft.DataColumn(ft.Text("ID Proveedor")),
            ft.DataColumn(ft.Text("ID Unidad"))
        ],
        rows=[],
        expand=True,
    )
    tabla_scroll = ft.Column(
        [tabla_resultado],
        scroll=ft.ScrollMode.ADAPTIVE, # Scroll vertical para las filas
        height=400, # Altura fija para el scroll vertical
        expand=True # La columna principal del scroll debe expandirse
    )

    # Función para limpiar los campos de entrada
    def limpiar_campos():
        codigo_articulo.value = ""
        nombre_articulo.value = ""
        precio.value = ""
        costo.value = ""
        existencia.value = ""
        idCategoria.value = ""
        idProveedor.value = ""
        idUnidad.value = ""
        page.update() # Actualizar la página para que los campos se borren

    def agregar_articulo(e):
        # Validar que ningún campo esté vacío
        if not all([codigo_articulo.value, nombre_articulo.value, precio.value, costo.value,
                    existencia.value, idCategoria.value, idProveedor.value, idUnidad.value]):
            mensaje.value = "Todos los campos son obligatorios."
            mensaje.color = "red"
            page.update()
            return

        try:
            # Validar tipos de datos numéricos
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
            
        conn = None # Inicializar conn a None
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO articulo (codigo_articulo, nombre, precio, costo, existencia, idCategoria, idproveedor, idUnidad)
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
            limpiar_campos() # Limpiar campos y actualizar la página
            consultar_articulos(None) # Vuelve a cargar la tabla para mostrar el nuevo artículo
        except mysql.connector.Error as err: # Captura errores específicos de MySQL
            mensaje.value = f"Error de base de datos: {err}"
            mensaje.color = "red"
        except Exception as ex:
            mensaje.value = f"Error inesperado: {str(ex)}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update() # Asegúrate de que los cambios en 'mensaje' se muestren

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
            # Verificar si el artículo existe antes de intentar eliminar
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
            limpiar_campos() # Limpiar campos y actualizar la página
            consultar_articulos(None) # Vuelve a cargar la tabla
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
            cursor.execute("SELECT codigo_articulo, nombre, precio, costo, existencia, idCategoria, idProveedor, idUnidad FROM articulo")
            resultados = cursor.fetchall()
            
            tabla_resultado.rows.clear() # Limpiar filas existentes
            for row in resultados:
                tabla_resultado.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]))
            
            mensaje.value = "Consulta realizada correctamente."
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

    fila_botones = ft.Row(
        [
            ft.ElevatedButton("Agregar", on_click=agregar_articulo),
            ft.ElevatedButton("Eliminar", on_click=eliminar_articulo),
            ft.ElevatedButton("Consultar", on_click=consultar_articulos)
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
        scroll= ft.ScrollMode.ALWAYS
    )