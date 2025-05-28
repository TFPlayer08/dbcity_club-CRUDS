import flet as ft
import mysql.connector
import datetime

def vista_ventas(page: ft.Page):
    def conectar_db():
        """Establece y retorna una conexión a la base de datos."""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="Toti#landia$7", # Asegúrate de que esta sea tu contraseña correcta
                database="dbcity_club"
            )
        except mysql.connector.Error as err:
            mensaje.value = f"Error al conectar a la base de datos: {err}"
            mensaje.color = "red"
            page.update()
            return None

    input_bg_color = "#E596CC"
    
    # --- Variables de estado de la venta ---
    # Store the currently fetched product's details for subtotal calculation
    current_product_details = {} 
    
    # Lista para almacenar los detalles de los productos en la venta actual
    # Cada elemento será un diccionario con: {codigo, nombre, cantidad, precio_unitario, subtotal}
    productos_en_venta = [] 

    # --- Componentes de la UI (Declaración adelantada para referenciarlos en funciones) ---
    txt_id_ventas = ft.TextField(label="ID Venta", bgcolor=input_bg_color, width=150)
    txt_fecha_venta = ft.TextField(label="Fecha Venta", bgcolor=input_bg_color, width=200, disabled=True)
    txt_id_cliente = ft.TextField(label="ID Cliente", bgcolor=input_bg_color, width=150)
    txt_id_empleado = ft.TextField(label="ID Empleado", bgcolor=input_bg_color, width=150)
    txt_id_metodo_pago = ft.TextField(label="ID Método Pago", bgcolor=input_bg_color, width=150)
    
    txt_codigo_articulo = ft.TextField(label="Código de Barras Artículo", bgcolor=input_bg_color, width=250)
    txt_cantidad = ft.TextField(label="Cantidad", bgcolor=input_bg_color, width=100)
    
    lbl_nombre_producto = ft.Text("Producto: ", size=16, weight=ft.FontWeight.BOLD)
    lbl_precio_unitario = ft.Text("Precio Unitario: $0.00", size=16, weight=ft.FontWeight.BOLD)
    lbl_stock_disponible = ft.Text("Stock Disponible: 0", size=16, weight=ft.FontWeight.BOLD)
    lbl_subtotal_producto = ft.Text("Subtotal Producto: $0.00", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    
    tabla_productos_venta = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cód. Artículo")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Precio Unitario")),
            ft.DataColumn(ft.Text("Subtotal")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
        expand=True,
        heading_row_color=ft.Colors.BLUE_GREY_100,
        data_row_color={"hovered": ft.Colors.BLUE_GREY_50},
        border_radius=ft.border_radius.all(8),
        border=ft.border.all(1, ft.Colors.BLUE_GREY_300),
    )

    lbl_total_venta = ft.Text("Total de Venta: $0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
    mensaje = ft.Text("", color="green", size=16)

    # Buttons for product actions (también declarados para poder habilitar/deshabilitar)
    btn_buscar_producto = ft.ElevatedButton(
        text="Buscar",
        icon=ft.Icons.SEARCH, 
        height=50,
        disabled=True 
    )
    btn_agregar_producto = ft.ElevatedButton(
        text="Agregar",
        icon=ft.Icons.ADD_SHOPPING_CART, 
        height=50,
        disabled=True 
    )
    btn_finalizar_venta = ft.ElevatedButton(
        text="Finalizar Venta",
        icon=ft.Icons.CHECK_CIRCLE, 
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
        disabled=True 
    )

    # --- Funciones de Lógica ---
    # Definir las funciones de lógica ANTES de asignarlas a los eventos de los componentes UI

    def toggle_sale_buttons():
        """Habilita/deshabilita los botones de producto y finalizar venta basándose en el ID Venta."""
        is_id_venta_entered = bool(txt_id_ventas.value)
        btn_buscar_producto.disabled = not is_id_venta_entered
        btn_agregar_producto.disabled = not is_id_venta_entered
        btn_finalizar_venta.disabled = not is_id_venta_entered
        # Deshabilitar el campo ID Venta una vez que se ha ingresado un valor
        txt_id_ventas.disabled = is_id_venta_entered and txt_id_ventas.value != ""
        page.update()

    def limpiar_campos_producto():
        """Limpia los campos de entrada de producto y las etiquetas de visualización."""
        txt_codigo_articulo.value = ""
        txt_cantidad.value = ""
        lbl_nombre_producto.value = "Producto: "
        lbl_precio_unitario.value = "Precio Unitario: $0.00"
        lbl_stock_disponible.value = "Stock Disponible: 0"
        lbl_subtotal_producto.value = "Subtotal Producto: $0.00"
        current_product_details.clear() # Limpiar detalles del producto almacenados
        page.update()

    def _on_load_view():
        """Inicializa la vista cuando se carga o se reinicia."""
        txt_fecha_venta.value = datetime.date.today().strftime("%Y-%m-%d")
        lbl_total_venta.value = "Total de Venta: $0.00"
        limpiar_campos_producto()
        productos_en_venta.clear()
        tabla_productos_venta.rows.clear()
        mensaje.value = ""
        current_product_details.clear() # Limpiar detalles del producto
        # Asegurarse de que los botones estén inicialmente deshabilitados si no hay ID de Venta
        toggle_sale_buttons() 
        page.update()

    def limpiar_campos_venta():
        """Limpia todos los campos principales de venta y reinicia los detalles del producto."""
        txt_id_ventas.value = ""
        txt_id_cliente.value = ""
        txt_id_empleado.value = ""
        txt_id_metodo_pago.value = ""
        # Volver a habilitar el campo id_ventas después de limpiar
        txt_id_ventas.disabled = False 
        _on_load_view() # Reinicia la fecha y la tabla de productos, y vuelve a deshabilitar los botones
        page.update()

    def calcular_total_venta():
        """Calcula y actualiza el monto total de la venta."""
        total = sum(item['subtotal'] for item in productos_en_venta)
        lbl_total_venta.value = f"Total de Venta: ${total:.2f}"
        page.update()

    def _on_cantidad_change(e):
        """Actualiza el subtotal del producto cuando cambia la entrada de cantidad."""
        try:
            cantidad = int(txt_cantidad.value) if txt_cantidad.value else 0
            if current_product_details and current_product_details.get('precio'):
                subtotal = cantidad * current_product_details['precio']
                lbl_subtotal_producto.value = f"Subtotal Producto: ${subtotal:.2f}"
            else:
                lbl_subtotal_producto.value = "Subtotal Producto: $0.00"
        except ValueError:
            lbl_subtotal_producto.value = "Subtotal Producto: $0.00"
        page.update()

    def buscar_producto_por_codigo(e, update_subtotal=False):
        """
        Busca un producto por código de barras y actualiza las etiquetas de información.
        Si `update_subtotal` es True, también intenta calcular el subtotal.
        """
        codigo = txt_codigo_articulo.value
        if not codigo:
            lbl_nombre_producto.value = "Producto: "
            lbl_precio_unitario.value = "Precio Unitario: $0.00"
            lbl_stock_disponible.value = "Stock Disponible: 0"
            lbl_subtotal_producto.value = "Subtotal Producto: $0.00"
            mensaje.value = "Ingresa un código de barras."
            mensaje.color = "red"
            current_product_details.clear() # Limpiar detalles del producto
            page.update()
            return
        
        conn = None
        try:
            conn = conectar_db()
            if not conn: return
            cursor = conn.cursor(dictionary=True) # Retorna filas como diccionarios
            cursor.execute("SELECT codigo_articulo, nombre, precio, existencia FROM articulo WHERE codigo_articulo = %s", (codigo,))
            articulo = cursor.fetchone()

            if articulo:
                lbl_nombre_producto.value = f"Producto: {articulo['nombre']}"
                lbl_precio_unitario.value = f"Precio Unitario: ${articulo['precio']:.2f}"
                lbl_stock_disponible.value = f"Stock Disponible: {articulo['existencia']}"
                mensaje.value = "" # Limpiar mensaje de error
                
                # Almacenar detalles recuperados para uso futuro (ej. cálculo de subtotal)
                current_product_details.update({
                    'codigo': articulo['codigo_articulo'], # Usar 'codigo' como clave para el código de artículo
                    'nombre': articulo['nombre'],
                    'precio': articulo['precio'],
                    'existencia': articulo['existencia']
                })

                if update_subtotal: # Solo actualizar subtotal si se solicita explícitamente o al cambiar la cantidad
                    _on_cantidad_change(None) # Recalcular subtotal basándose en la cantidad actual
            else:
                lbl_nombre_producto.value = "Producto: No encontrado"
                lbl_precio_unitario.value = "Precio Unitario: $0.00"
                lbl_stock_disponible.value = "Stock Disponible: 0"
                lbl_subtotal_producto.value = "Subtotal Producto: $0.00"
                mensaje.value = "Artículo no encontrado."
                mensaje.color = "red"
                current_product_details.clear() # Limpiar detalles del producto
            page.update()

        except mysql.connector.Error as err:
            mensaje.value = f"Error de base de datos al buscar artículo: {err}"
            mensaje.color = "red"
            page.update()
        except Exception as ex:
            mensaje.value = f"Error inesperado al buscar artículo: {str(ex)}"
            mensaje.color = "red"
            page.update()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def agregar_producto_a_venta(e):
        """Añade un producto a la lista de la venta y actualiza la UI."""
        if not txt_id_ventas.value:
            mensaje.value = "Primero ingresa el ID de Venta."
            mensaje.color = "red"
            page.update()
            return

        codigo = txt_codigo_articulo.value
        cantidad_str = txt_cantidad.value

        if not codigo or not cantidad_str:
            mensaje.value = "Ingresa código de barras y cantidad."
            mensaje.color = "red"
            page.update()
            return
        
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                mensaje.value = "La cantidad debe ser un número positivo."
                mensaje.color = "red"
                page.update()
                return
        except ValueError:
            mensaje.value = "La cantidad debe ser un número entero."
            mensaje.color = "red"
            page.update()
            return
        
        # Usar current_product_details si está disponible, de lo contrario buscar de nuevo
        articulo_info = current_product_details
        if not articulo_info or articulo_info.get('codigo') != codigo:
            # Si los detalles no están actualizados o no coinciden, volver a buscarlos
            conn = conectar_db()
            if not conn: return
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT codigo_articulo, nombre, precio, existencia FROM articulo WHERE codigo_articulo = %s", (codigo,))
            articulo_info_from_db = cursor.fetchone() # Usar un nombre diferente para evitar confusión

            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            
            if not articulo_info_from_db:
                mensaje.value = "Artículo no encontrado."
                mensaje.color = "red"
                page.update()
                return
            
            # Si se encontró en la DB, actualizar articulo_info para usarlo en esta adición
            articulo_info = {
                'codigo': articulo_info_from_db['codigo_articulo'],
                'nombre': articulo_info_from_db['nombre'],
                'precio': articulo_info_from_db['precio'],
                'existencia': articulo_info_from_db['existencia']
            }
            # Opcional: Actualizar current_product_details aquí también si quieres mantenerlo sincronizado
            current_product_details.update(articulo_info)


        # Verificar stock
        if cantidad > articulo_info['existencia']:
            mensaje.value = f"No hay suficiente stock. Disponible: {articulo_info['existencia']}"
            mensaje.color = "red"
            page.update()
            return

        subtotal_item = cantidad * articulo_info['precio']
        
        # Comprobar si el producto ya está en la lista de venta y actualizar cantidad/subtotal
        producto_existente = next((p for p in productos_en_venta if p['codigo'] == codigo), None)

        if producto_existente:
            nueva_cantidad = producto_existente['cantidad'] + cantidad
            if nueva_cantidad > articulo_info['existencia']:
                mensaje.value = f"No puedes agregar más. Stock disponible: {articulo_info['existencia']}. Cantidad en venta: {producto_existente['cantidad']}"
                mensaje.color = "red"
                page.update()
                return
            producto_existente['cantidad'] = nueva_cantidad
            producto_existente['subtotal'] = nueva_cantidad * articulo_info['precio']
        else:
            productos_en_venta.append({
                'codigo': articulo_info['codigo'], # ¡CORREGIDO AQUÍ! Usar la clave 'codigo'
                'nombre': articulo_info['nombre'],
                'cantidad': cantidad,
                'precio_unitario': articulo_info['precio'],
                'subtotal': subtotal_item
            })
            
        actualizar_tabla_productos_venta()
        calcular_total_venta()
        limpiar_campos_producto() # Limpiar entrada de producto para el siguiente artículo
        txt_codigo_articulo.focus() # Enfocar para el siguiente escaneo de código de barras
        mensaje.value = "Producto agregado."
        mensaje.color = "green"
        page.update()

    def eliminar_producto_de_venta(e):
        """Elimina un producto de la lista de la venta."""
        codigo_a_eliminar = e.control.data # El 'data' del botón contiene el código del producto
        initial_len = len(productos_en_venta)
        productos_en_venta[:] = [p for p in productos_en_venta if p['codigo'] != codigo_a_eliminar]
        
        if len(productos_en_venta) < initial_len: # Verificar si se eliminó algo
            actualizar_tabla_productos_venta()
            calcular_total_venta()
            mensaje.value = f"Producto {codigo_a_eliminar} eliminado de la venta."
            mensaje.color = "green"
        else:
            mensaje.value = f"Error: Producto {codigo_a_eliminar} no encontrado en la lista."
            mensaje.color = "red"
        page.update()

    def actualizar_tabla_productos_venta():
        """Actualiza la tabla de datos con los productos actuales en venta."""
        tabla_productos_venta.rows.clear()
        for item in productos_en_venta:
            tabla_productos_venta.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['codigo'])),
                        ft.DataCell(ft.Text(item['nombre'])),
                        ft.DataCell(ft.Text(str(item['cantidad']))),
                        ft.DataCell(ft.Text(f"${item['precio_unitario']:.2f}")),
                        ft.DataCell(ft.Text(f"${item['subtotal']:.2f}")),
                        ft.DataCell(ft.IconButton(
                            icon=ft.Icons.DELETE, 
                            icon_color=ft.Colors.RED_500,
                            tooltip="Eliminar producto de la venta",
                            on_click=eliminar_producto_de_venta,
                            data=item['codigo'] # Pasa el código para identificar el artículo a eliminar
                        )),
                    ]
                )
            )
        page.update() # Actualizar la tabla en la UI

    def finalizar_venta(e):
        """Finaliza la venta, guarda en la DB y limpia la vista."""
        id_venta = txt_id_ventas.value
        id_cliente = txt_id_cliente.value
        id_empleado = txt_id_empleado.value
        id_metodo_pago = txt_id_metodo_pago.value
        # Obtener la fecha actual al momento de finalizar la venta para asegurar el formato correcto
        fecha_venta = datetime.date.today().strftime("%Y-%m-%d") 
        
        try:
            total_venta = float(lbl_total_venta.value.replace("Total de Venta: $", ""))
        except ValueError:
            mensaje.value = "El total de venta no es un número válido."
            mensaje.color = "red"
            page.update()
            return

        if not id_venta or not id_cliente or not id_empleado or not id_metodo_pago:
            mensaje.value = "Faltan datos de la venta (ID Venta, Cliente, Empleado, Método Pago)."
            mensaje.color = "red"
            page.update()
            return
        
        if not productos_en_venta:
            mensaje.value = "No hay productos en la venta para finalizar."
            mensaje.color = "red"
            page.update()
            return
        
        conn = None
        try:
            conn = conectar_db()
            if not conn: return
            cursor = conn.cursor()
            conn.start_transaction() # Iniciar transacción para atomicidad

            # 1. Insertar en la tabla 'ventas'
            sql_venta = """
                INSERT INTO ventas (idVentas, fecha, idCliente, idempleados, idmetodo_pago, importe)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_venta, (id_venta, fecha_venta, id_cliente, id_empleado, id_metodo_pago, total_venta))

            # 2. Insertar en la tabla 'descventa' (detalle de la venta) y actualizar existencia en 'articulo'
            sql_descventa = """
                INSERT INTO descventa (idventas, codigo_articulo, cantidad, total)
                VALUES (%s, %s, %s, %s)
            """
            sql_actualizar_stock = """
                UPDATE articulo SET existencia = existencia - %s WHERE codigo_articulo = %s
            """
            for item in productos_en_venta:
                cursor.execute(sql_descventa, (id_venta, item['codigo'], item['cantidad'], item['subtotal']))
                cursor.execute(sql_actualizar_stock, (item['cantidad'], item['codigo'])) 

            conn.commit() # Confirmar todas las operaciones
            mensaje.value = "Venta finalizada y guardada correctamente."
            mensaje.color = "green"
            limpiar_campos_venta() # Limpiar toda la interfaz después de la venta exitosa
        
        except mysql.connector.Error as err:
            conn.rollback() # Deshacer si hay algún error
            if err.errno == 1062: # Entrada duplicada para la clave primaria 'idVentas' (o la clave compuesta en descventa)
                mensaje.value = f"Error: La venta con ID {id_venta} o uno de sus productos ya existe. Intenta con otro ID de venta."
            else:
                mensaje.value = f"Error de base de datos al finalizar venta: {err}"
            mensaje.color = "red"
        except Exception as ex:
            if conn and conn.is_connected():
                conn.rollback() # Deshacer si hay algún error inesperado
            mensaje.value = f"Error inesperado al finalizar venta: {str(ex)}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    # --- Asignación de Eventos después de la definición de funciones y componentes ---
    txt_id_ventas.on_change = lambda e: toggle_sale_buttons()
    txt_id_ventas.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")

    txt_id_cliente.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
    txt_id_empleado.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
    txt_id_metodo_pago.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")

    txt_codigo_articulo.on_change = lambda e: buscar_producto_por_codigo(e, update_subtotal=True)
    txt_codigo_articulo.on_submit = lambda e: agregar_producto_a_venta(e) # Agrega producto al presionar Enter en código de barras

    txt_cantidad.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
    txt_cantidad.on_change = lambda e: _on_cantidad_change(e)
    txt_cantidad.on_submit = lambda e: agregar_producto_a_venta(e) # Agrega producto al presionar Enter en cantidad

    btn_buscar_producto.on_click = lambda e: buscar_producto_por_codigo(e, update_subtotal=True)
    btn_agregar_producto.on_click = agregar_producto_a_venta
    btn_finalizar_venta.on_click = finalizar_venta

    # Contenedor para el scroll de la tabla de productos de la venta
    tabla_productos_venta_scroll_container = ft.Column(
        [tabla_productos_venta],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=300, # Altura fija para el área de la tabla
        expand=True,
    )

    # Se llama a _on_load_view cuando la vista se carga inicialmente
    def on_view_change_handler(e):
        if e.route == "/ventas":
            _on_load_view()
        # Puedes añadir lógica para limpiar/guardar el estado si sales de la vista
        # else:
        #     pass 
            
    page.on_view_change = on_view_change_handler
    
    # --- Diseño de la UI ---
    return ft.Column(
        [
            ft.Text("Registro de Ventas", size=28, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    txt_id_ventas,
                    txt_fecha_venta,
                    txt_id_cliente,
                    txt_id_empleado,
                    txt_id_metodo_pago,
                ],
                wrap=True, # Permite que los campos se envuelvan si la pantalla es pequeña
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(),
            ft.Text("Agregar Productos", size=22, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    txt_codigo_articulo,
                    btn_buscar_producto, 
                    txt_cantidad,
                    btn_agregar_producto, 
                ],
                wrap=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    lbl_nombre_producto,
                    lbl_precio_unitario,
                    lbl_stock_disponible,
                    lbl_subtotal_producto,
                ],
                wrap=True,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            ft.Divider(),
            ft.Text("Detalle de Venta", size=22, weight=ft.FontWeight.BOLD),
            tabla_productos_venta_scroll_container, # Contenedor para la tabla con scroll
            ft.Row(
                [
                    lbl_total_venta,
                    btn_finalizar_venta, 
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Total a la izquierda, botón a la derecha
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            mensaje,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START, # Empieza desde arriba
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ADAPTIVE, # Permite scroll a toda la vista si es necesario
        expand=True,
    )