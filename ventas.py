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
                password="Toti#landia$7",
                database="dbcity_club"
            )
        except mysql.connector.Error as err:
            mensaje.value = f"Error al conectar a la base de datos: {err}"
            mensaje.color = "red"
            page.update()
            return None

    input_bg_color = "#E596CC"
    
    # Variables de estado
    current_product_details = {} 
    productos_en_venta = [] 
    metodos_pago = []
    cliente_info = {}

    # --- Componentes de la UI ---
    # Campo para ID Cliente con búsqueda
    txt_id_cliente = ft.TextField(
        label="ID Cliente", 
        bgcolor=input_bg_color, 
        width=150,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
    )
    
    # Información del cliente
    lbl_nombre_cliente = ft.Text("Nombre: ", size=16)
    lbl_telefono_cliente = ft.Text("Teléfono: ", size=16)
    lbl_membresia_cliente = ft.Text("Membresía: ", size=16)
    lbl_tipo_membresia = ft.Text("Tipo: ", size=16)
    
    # Dropdown para método de pago
    dd_metodo_pago = ft.Dropdown(
        label="Método de Pago",
        bgcolor=input_bg_color,
        width=250,
        options=[],
        autofocus=True
    )
    
    txt_id_empleado = ft.TextField(
        label="ID Empleado", 
        bgcolor=input_bg_color, 
        width=150,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
    )
    
    # Campos para productos
    txt_codigo_articulo = ft.TextField(
        label="Código de Barras Artículo", 
        bgcolor=input_bg_color, 
        width=250,
        autofocus=True
    )
    txt_cantidad = ft.TextField(
        label="Cantidad", 
        bgcolor=input_bg_color, 
        width=100,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""),
        value="1"  # Valor por defecto
    )
    
    # Etiquetas de información del producto
    lbl_nombre_producto = ft.Text("Producto: ", size=16, weight=ft.FontWeight.BOLD)
    lbl_precio_unitario = ft.Text("Precio Unitario: $0.00", size=16, weight=ft.FontWeight.BOLD)
    lbl_stock_disponible = ft.Text("Stock Disponible: 0", size=16, weight=ft.FontWeight.BOLD)
    lbl_subtotal_producto = ft.Text("Subtotal Producto: $0.00", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    
    # Tabla de productos en venta
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

    # Total y mensajes
    lbl_total_venta = ft.Text("Total de Venta: $0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
    mensaje = ft.Text("", color="green", size=16)

    # Botones
    btn_buscar_cliente = ft.ElevatedButton(
        text="Buscar Cliente",
        icon=ft.Icons.SEARCH,
        height=50,
        on_click=lambda e: buscar_cliente(e)
    )
    
    btn_buscar_producto = ft.ElevatedButton(
        text="Buscar",
        icon=ft.Icons.SEARCH, 
        height=50,
        on_click=lambda e: buscar_producto_por_codigo(e, update_subtotal=True)
    )
    
    btn_agregar_producto = ft.ElevatedButton(
        text="Agregar",
        icon=ft.Icons.ADD_SHOPPING_CART, 
        height=50,
        on_click=lambda e: agregar_producto_a_venta(e)
    )
    
    btn_finalizar_venta = ft.ElevatedButton(
        text="Finalizar Venta",
        icon=ft.Icons.CHECK_CIRCLE, 
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
        on_click=lambda e: finalizar_venta(e)
    )

    # --- Funciones de Lógica ---
    def cargar_metodos_pago():
        """Carga los métodos de pago desde la base de datos"""
        conn = None
        try:
            conn = conectar_db()
            if not conn: return
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT idmetodo_pago, nombre_del_pago FROM metodo_pago")
            global metodos_pago
            metodos_pago = cursor.fetchall()
            
            dd_metodo_pago.options.clear()
            for metodo in metodos_pago:
                dd_metodo_pago.options.append(
                    ft.dropdown.Option(
                        key=str(metodo['idmetodo_pago']),
                        text=metodo['nombre_del_pago']
                    )
                )
            page.update()
            
        except mysql.connector.Error as err:
            mensaje.value = f"Error al cargar métodos de pago: {err}"
            mensaje.color = "red"
            page.update()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def buscar_cliente(e):
        """Busca un cliente por ID y muestra su información"""
        id_cliente = txt_id_cliente.value
        if not id_cliente:
            mensaje.value = "Ingresa un ID de cliente"
            mensaje.color = "red"
            page.update()
            return
        
        conn = None
        try:
            conn = conectar_db()
            if not conn: return
            cursor = conn.cursor(dictionary=True)
            
            # Buscar información básica del cliente
            cursor.execute("""
                SELECT nombre, telefono 
                FROM Cliente 
                WHERE idCliente = %s
            """, (id_cliente,))
            cliente = cursor.fetchone()
            
            if not cliente:
                limpiar_info_cliente()
                mensaje.value = "Cliente no encontrado"
                mensaje.color = "red"
                page.update()
                return
            
            # Buscar información de membresía
            cursor.execute("""
                SELECT codigo, tipo_membresia 
                FROM Membresia 
                WHERE idCliente = %s
                ORDER BY fecha_vigencia DESC
                LIMIT 1
            """, (id_cliente,))
            membresia = cursor.fetchone()
            
            # Actualizar la UI con la información del cliente
            lbl_nombre_cliente.value = f"Nombre: {cliente['nombre']}"
            lbl_telefono_cliente.value = f"Teléfono: {cliente['telefono']}"
            
            if membresia:
                lbl_membresia_cliente.value = f"Membresía: {membresia['codigo']}"
                lbl_tipo_membresia.value = f"Tipo: {membresia['tipo_membresia']}"
            else:
                lbl_membresia_cliente.value = "Membresía: Sin membresía activa"
                lbl_tipo_membresia.value = "Tipo: -"
            
            mensaje.value = "Cliente encontrado"
            mensaje.color = "green"
            cliente_info.update({
                'id': id_cliente,
                'nombre': cliente['nombre'],
                'telefono': cliente['telefono'],
                'membresia': membresia['codigo'] if membresia else None,
                'tipo_membresia': membresia['tipo_membresia'] if membresia else None
            })
            
        except mysql.connector.Error as err:
            mensaje.value = f"Error al buscar cliente: {err}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    def limpiar_info_cliente():
        """Limpia la información del cliente mostrada"""
        lbl_nombre_cliente.value = "Nombre: "
        lbl_telefono_cliente.value = "Teléfono: "
        lbl_membresia_cliente.value = "Membresía: "
        lbl_tipo_membresia.value = "Tipo: "
        cliente_info.clear()

    def limpiar_campos_producto():
        """Limpia los campos de entrada de producto y las etiquetas de visualización."""
        txt_codigo_articulo.value = ""
        txt_cantidad.value = "1"  # Resetear a 1 en lugar de vacío
        lbl_nombre_producto.value = "Producto: "
        lbl_precio_unitario.value = "Precio Unitario: $0.00"
        lbl_stock_disponible.value = "Stock Disponible: 0"
        lbl_subtotal_producto.value = "Subtotal Producto: $0.00"
        current_product_details.clear()
        page.update()

    def _on_load_view():
        """Inicializa la vista cuando se carga o se reinicia."""
        lbl_total_venta.value = "Total de Venta: $0.00"
        limpiar_campos_producto()
        limpiar_info_cliente()
        productos_en_venta.clear()
        tabla_productos_venta.rows.clear()
        mensaje.value = ""
        current_product_details.clear()
        txt_id_cliente.value = ""
        txt_id_empleado.value = ""
        dd_metodo_pago.value = None
        cargar_metodos_pago()
        page.update()

    def limpiar_campos_venta():
        """Limpia todos los campos principales de venta y reinicia los detalles del producto."""
        _on_load_view()

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
        """Busca un producto por código de barras y actualiza las etiquetas de información."""
        codigo = txt_codigo_articulo.value
        if not codigo:
            lbl_nombre_producto.value = "Producto: "
            lbl_precio_unitario.value = "Precio Unitario: $0.00"
            lbl_stock_disponible.value = "Stock Disponible: 0"
            lbl_subtotal_producto.value = "Subtotal Producto: $0.00"
            mensaje.value = "Ingresa un código de barras."
            mensaje.color = "red"
            current_product_details.clear()
            page.update()
            return
        
        conn = None
        try:
            conn = conectar_db()
            if not conn: return
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT codigo_articulo, nombre, precio, existencia FROM articulo WHERE codigo_articulo = %s", (codigo,))
            articulo = cursor.fetchone()

            if articulo:
                lbl_nombre_producto.value = f"Producto: {articulo['nombre']}"
                lbl_precio_unitario.value = f"Precio Unitario: ${articulo['precio']:.2f}"
                lbl_stock_disponible.value = f"Stock Disponible: {articulo['existencia']}"
                mensaje.value = ""
                
                current_product_details.update({
                    'codigo': articulo['codigo_articulo'],
                    'nombre': articulo['nombre'],
                    'precio': articulo['precio'],
                    'existencia': articulo['existencia']
                })

                if update_subtotal:
                    _on_cantidad_change(None)
            else:
                lbl_nombre_producto.value = "Producto: No encontrado"
                lbl_precio_unitario.value = "Precio Unitario: $0.00"
                lbl_stock_disponible.value = "Stock Disponible: 0"
                lbl_subtotal_producto.value = "Subtotal Producto: $0.00"
                mensaje.value = "Artículo no encontrado."
                mensaje.color = "red"
                current_product_details.clear()
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
        if not txt_id_cliente.value:
            mensaje.value = "Primero ingresa el ID del Cliente."
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
        
        articulo_info = current_product_details
        if not articulo_info or articulo_info.get('codigo') != codigo:
            conn = conectar_db()
            if not conn: return
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT codigo_articulo, nombre, precio, existencia FROM articulo WHERE codigo_articulo = %s", (codigo,))
            articulo_info_from_db = cursor.fetchone()

            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            
            if not articulo_info_from_db:
                mensaje.value = "Artículo no encontrado."
                mensaje.color = "red"
                page.update()
                return
            
            articulo_info = {
                'codigo': articulo_info_from_db['codigo_articulo'],
                'nombre': articulo_info_from_db['nombre'],
                'precio': articulo_info_from_db['precio'],
                'existencia': articulo_info_from_db['existencia']
            }
            current_product_details.update(articulo_info)

        if cantidad > articulo_info['existencia']:
            mensaje.value = f"No hay suficiente stock. Disponible: {articulo_info['existencia']}"
            mensaje.color = "red"
            page.update()
            return

        subtotal_item = cantidad * articulo_info['precio']
        
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
                'codigo': articulo_info['codigo'],
                'nombre': articulo_info['nombre'],
                'cantidad': cantidad,
                'precio_unitario': articulo_info['precio'],
                'subtotal': subtotal_item
            })
            
        actualizar_tabla_productos_venta()
        calcular_total_venta()
        limpiar_campos_producto()
        txt_codigo_articulo.focus()
        mensaje.value = "Producto agregado."
        mensaje.color = "green"
        page.update()

    def eliminar_producto_de_venta(e):
        """Elimina un producto de la lista de la venta."""
        codigo_a_eliminar = e.control.data
        initial_len = len(productos_en_venta)
        productos_en_venta[:] = [p for p in productos_en_venta if p['codigo'] != codigo_a_eliminar]
        
        if len(productos_en_venta) < initial_len:
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
                            data=item['codigo']
                        )),
                    ]
                )
            )
        page.update()

    def finalizar_venta(e):
        """Finaliza la venta, guarda en la DB y limpia la vista."""
        id_cliente = txt_id_cliente.value
        id_empleado = txt_id_empleado.value
        metodo_pago_id = dd_metodo_pago.value
        fecha_venta = datetime.date.today().strftime("%Y-%m-%d") 
        
        try:
            total_venta = float(lbl_total_venta.value.replace("Total de Venta: $", ""))
        except ValueError:
            mensaje.value = "El total de venta no es un número válido."
            mensaje.color = "red"
            page.update()
            return

        if not id_cliente or not id_empleado or not metodo_pago_id:
            mensaje.value = "Faltan datos de la venta (Cliente, Empleado, Método Pago)."
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
            conn.start_transaction()

            # 1. Insertar en la tabla 'ventas' (el ID es autoincrement)
            sql_venta = """
                INSERT INTO ventas (fecha, idCliente, idempleados, idmetodo_pago, importe)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_venta, (fecha_venta, id_cliente, id_empleado, metodo_pago_id, total_venta))
            
            # Obtener el ID de la venta recién insertada
            venta_id = cursor.lastrowid

            # 2. Insertar en la tabla 'descventa' (ahora incluyendo el precio) y actualizar stock
            sql_descventa = """
                INSERT INTO descventa (idventas, codigo_articulo, cantidad, precio, total)
                VALUES (%s, %s, %s, %s, %s)
            """
            sql_actualizar_stock = """
                UPDATE articulo SET existencia = existencia - %s WHERE codigo_articulo = %s
            """
            for item in productos_en_venta:
                cursor.execute(sql_descventa, (
                    venta_id, 
                    item['codigo'], 
                    item['cantidad'], 
                    item['precio_unitario'],  # Precio unitario del artículo
                    item['subtotal']          # Total (precio * cantidad)
                ))
                cursor.execute(sql_actualizar_stock, (item['cantidad'], item['codigo'])) 

            conn.commit()
            mensaje.value = f"Venta #{venta_id} finalizada y guardada correctamente."
            mensaje.color = "green"
            limpiar_campos_venta()
        
        except mysql.connector.Error as err:
            if conn and conn.is_connected():
                conn.rollback()
            mensaje.value = f"Error de base de datos al finalizar venta: {err}"
            mensaje.color = "red"
        except Exception as ex:
            if conn and conn.is_connected():
                conn.rollback()
            mensaje.value = f"Error inesperado al finalizar venta: {str(ex)}"
            mensaje.color = "red"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            page.update()

    # --- Configuración inicial ---
    _on_load_view()

    # --- Asignación de Eventos ---
    txt_codigo_articulo.on_change = lambda e: buscar_producto_por_codigo(e, update_subtotal=True)
    txt_codigo_articulo.on_submit = lambda e: agregar_producto_a_venta(e)

    txt_cantidad.on_change = lambda e: _on_cantidad_change(e)
    txt_cantidad.on_submit = lambda e: agregar_producto_a_venta(e)

    # --- Diseño de la UI ---
    # Contenedor para el scroll de la tabla de productos de la venta
    tabla_productos_venta_scroll_container = ft.Column(
        [tabla_productos_venta],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=300,
        expand=True,
    )

    # Sección de información del cliente
    cliente_info_container = ft.Column(
        [
            ft.Row([txt_id_cliente, btn_buscar_cliente]),
            ft.Row([lbl_nombre_cliente, lbl_telefono_cliente]),
            ft.Row([lbl_membresia_cliente, lbl_tipo_membresia])
        ],
        spacing=10
    )

    # Sección de información del producto
    producto_info_container = ft.Row(
        [
            lbl_nombre_producto,
            lbl_precio_unitario,
            lbl_stock_disponible,
            lbl_subtotal_producto,
        ],
        wrap=True,
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )

    # Sección principal de la vista
    return ft.Column(
        [
            ft.Text("Registro de Ventas", size=28, weight=ft.FontWeight.BOLD),
            
            # Sección de datos de la venta
            ft.Column(
                [
                    ft.Row(
                        [
                            cliente_info_container,
                            txt_id_empleado,
                            dd_metodo_pago,
                        ],
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=10
            ),
            
            ft.Divider(),
            
            # Sección para agregar productos
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
            producto_info_container,
            
            ft.Divider(),
            
            # Sección de detalle de venta
            ft.Text("Detalle de Venta", size=22, weight=ft.FontWeight.BOLD),
            tabla_productos_venta_scroll_container,
            
            # Total y botón finalizar
            ft.Row(
                [
                    lbl_total_venta,
                    btn_finalizar_venta, 
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            mensaje,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
    )