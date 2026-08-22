from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from articulos.dao.inventariodao import InventarioDAO
from articulos.models import Producto, Categoria


@csrf_exempt
def dashboard_retail(request):
    pestaana = request.GET.get('pestaana', 'tablero')
    usuario_activo = request.GET.get('usuario', 'E. Moncada')
    siguiente_usuario = (
        "Sergio Salcedo" if usuario_activo == "E. Moncada" else "E. Moncada"
    )

    # Asegurar que existan categorías base en la base de datos para las pruebas
    if not Categoria.objects.exists():
        Categoria.objects.create(
            nombre="Ropa", descripcion="Prendas de vestir"
        )
        Categoria.objects.create(
            nombre="Calzado", descripcion="Zapatos y tenis"
        )
        Categoria.objects.create(
            nombre="Accesorios", descripcion="Gorras y mochilas"
        )

    # PROCESAMIENTO DE ENVÍO DE FORMULARIOS (ALTAS, BAJAS Y CAMBIOS REALES)
    mensaje_alerta = ""
    if request.method == "POST":
        accion = request.POST.get('accion')

        if accion == "guardar_producto":
            sku = request.POST.get('sku')
            nombre = request.POST.get('nombre')
            categoria_nombre = request.POST.get('categoria')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')

            try:
                cat = Categoria.objects.get(nombre=categoria_nombre)
                InventarioDAO.insertar_nuevo_producto(
                    sku=sku, nombre=nombre, categoria_id=cat.id,
                    precio=precio, stock_inicial=stock, stock_min=5
                )
                return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")
            except Exception as e:
                mensaje_alerta = f"Error al guardar producto: {str(e)}"

        elif accion == "procesar_movimiento":
            sku_afectado = request.POST.get('sku_afectado')
            tipo_flujo = request.POST.get('tipo_flujo')

            try:
                cantidad = int(request.POST.get('cantidad', 0))
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor que cero")

                prod = Producto.objects.get(sku=sku_afectado)
                if "Entrada" in tipo_flujo:
                    prod.stock_actual += cantidad
                else:
                    if cantidad > prod.stock_actual:
                        raise ValueError(
                            "La salida no puede superar el stock actual"
                        )
                    prod.stock_actual -= cantidad
                prod.save()
                return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")
            except Exception as e:
                mensaje_alerta = f"Error en movimiento: {str(e)}"

        elif accion == "eliminar_producto":
            sku_a_borrar = request.POST.get('sku_a_borrar')
            try:
                prod = Producto.objects.get(sku=sku_a_borrar)
                # Remueve físicamente el registro de db.sqlite3
                prod.delete()
                return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")
            except Exception as e:
                mensaje_alerta = f"Error al eliminar: {str(e)}"

    # EXTRACCIÓN DE DATOS REALES MEDIANTE EL PATRÓN DAO
    productos_db = InventarioDAO.obtener_todo_el_inventario()

    # Estilos CSS de la interfaz
    estilos = f"""
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f3f4f6;
            margin: 0;
            padding: 0;
            color: #1f2937;
        }}
        nav {{
            background-color: #1e3a8a;
            padding: 16px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .nav-brand {{
            font-size: 20px; font-weight: bold; display: flex;
            align-items: center; gap: 8px;
        }}
        .nav-links {{ display: flex; gap: 24px; font-size: 14px;
            align-items: center; }}
        .nav-links a {{ color: white; text-decoration: none;
            font-weight: 500; }}
        .nav-links a:hover, .nav-links a.active {{ color: #93c5fd;
            text-decoration: underline; }}
        .nav-user-block {{
            display: flex; align-items: center; gap: 12px;
            border-left: 1px solid #1e40af; padding-left: 16px;
        }}
        .nav-user {{ color: #bfdbfe; font-weight: 500; }}
        .btn-switch {{ background-color: #2563eb; color: white;
            font-size: 13px;
            padding: 6px 12px; border: 1px solid #60a5fa; border-radius: 4px;
            cursor: pointer; text-decoration: none; }}
        main {{ max-width: 1200px; margin: 32px auto; padding: 0 16px; }}
        .card {{ background-color: white; padding: 24px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 8px; }}
        .card-header {{ display: flex; justify-content: space-between;
            align-items: center; margin-bottom: 24px; }}
        h1 {{ font-size: 24px; font-weight: bold; color: #111827; margin: 0; }}
        .subtitle {{ font-size: 14px; color: #6b7280; margin-top: 4px; }}
        .btn {{ background-color: #2563eb; color: white; font-weight: 500;
            font-size: 14px; padding: 10px 20px; border: none;
            border-radius: 4px; cursor: pointer; text-decoration: none;
            display: inline-block; }}
        .btn:hover {{ background-color: #1d4ed8; }}
        .btn-danger {{ background-color: #ef4444; padding: 6px 12px;
            font-size: 12px; font-weight: 600; border: none;
            border-radius: 4px;
            color: white; cursor: pointer; }}
        .btn-danger:hover {{ background-color: #dc2626; }}
        .alert {{
            background-color: #fef2f2; border-left: 4px solid #ef4444;
            padding: 16px; border-radius: 0 4px 4px 0;
            margin-bottom: 24px; display: flex; gap: 12px;
        }}
        .alert-title {{ font-size: 14px; font-weight: 600;
            color: #991b1b; margin: 0; }}
        .alert-desc {{ font-size: 12px; color: #b91c1c; margin-top: 4px; }}
        .table-container {{ overflow-x: auto; margin-top: 16px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left;
            font-size: 14px; }}
        th {{ background-color: #f9fafb; padding: 12px 24px; font-weight: 600;
            color: #4b5563; border-bottom: 1px solid #e5e7eb; }}
        td {{ padding: 16px 24px; border-bottom: 1px solid #e5e7eb; }}
        .sku {{ font-family: monospace; font-weight: bold; color: #1d4ed8; }}
        .badge-optimo {{ background-color: #d1fae5; color: #065f46;
            padding: 4px 10px; border-radius: 9999px; font-size: 12px;
            font-weight: 600; }}
        .badge-critico {{
            background-color: #fee2e2; color: #991b1b; padding: 4px 10px;
            border-radius: 9999px; font-size: 12px; font-weight: 600;
        }}
        .form-group {{ margin-bottom: 16px; display: flex;
            flex-direction: column; gap: 6px; }}
    </style>
    """

    contenido_pantalla = ""
    error_bloque = (
        f'<div class="alert"><p class="alert-title">{mensaje_alerta}</p></div>'
        if mensaje_alerta
        else ""
    )

    if pestaana == 'registro':
        contenido_pantalla = f"""
        {error_bloque}
        <div class="card">
            <div class="card-header">
                <div>
                    <h1>➕ Registrar Nuevo Producto de Retail</h1>
                    <div class="subtitle">
                        Asignación de claves SKU y existencias iniciales
                        (Operador: {usuario_activo}).
                    </div>
                </div>
                <a
                    href="?pestaana=tablero&usuario={usuario_activo}"
                    class="btn"
                    style="background-color: #4b5563;"
                >⬅️ Volver</a>
            </div>
            <form
                method="POST"
                action="?pestaana=registro&usuario={usuario_activo}"
                style="max-width: 600px; margin-top: 24px;"
            >
                <input type="hidden" name="accion" value="guardar_producto">
                <div class="form-group">
                    <label>Código SKU Universal:</label>
                    <input
                        type="text"
                        name="sku"
                        placeholder="Ej. PROD-100"
                        required
                    >
                </div>
                <div class="form-group">
                    <label>Descripción / Nombre del Artículo:</label>
                    <input
                        type="text"
                        name="nombre"
                        placeholder="Ej. Mochila Ejecutiva"
                        required
                    >
                </div>
                <div class="form-group">
                    <label>Categoría Logística:</label>
                    <select name="categoria">
                        <option>Ropa</option>
                        <option>Calzado</option>
                        <option>Accesorios</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Precio Unitario ($):</label>
                    <input type="number" step="0.01" name="precio" required>
                </div>
                <div class="form-group">
                    <label>Existencias Iniciales:</label>
                    <input type="number" name="stock" required>
                </div>
                <button
                    type="submit"
                    class="btn"
                    style="margin-top: 12px; width: 100%;"
                >💾 Guardar Producto Real</button>
            </form>
        </div>
        """
    elif pestaana == 'movimientos':
        opciones_productos = "".join(
            [
                f'<option value="{p.sku}">{p.sku} - {p.nombre} '
                f'(Actual: {p.stock_actual} pzas)</option>'
                for p in productos_db
            ]
        )
        if not opciones_productos:
            opciones_productos = (
                '<option value="">No hay productos en base de datos</option>'
            )

        contenido_pantalla = f"""
        {error_bloque}
        <div class="card">
            <div class="card-header">
                <div>
                    <h1>📦 Registro de Movimientos de Almacén</h1>
                    <div class="subtitle">
                        Modifica existencias reales mediante operaciones de
                        entradas y salidas.
                    </div>
                </div>
            </div>
            <form
                method="POST"
                action="?pestaana=movimientos&usuario={usuario_activo}"
                style="max-width: 600px; margin: 24px 0;"
            >
                <input type="hidden" name="accion" value="procesar_movimiento">
                <div class="form-group">
                    <label>
                        Seleccionar Artículo de la Base de Datos:
                    </label>
                    <select name="sku_afectado">{opciones_productos}</select>
                </div>
                <div class="form-group">
                    <label>Tipo de Flujo:</label>
                    <select name="tipo_flujo">
                        <option>🔺 Entrada (Abastecimiento)</option>
                        <option>🔻 Salida (Venta)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Cantidad:</label>
                    <input
                        type="number"
                        name="cantidad"
                        min="1"
                        required
                    >
                </div>
                <button type="submit" class="btn">Registrar Movimiento</button>
            </form>
        </div>
        """
    else:
        filas_productos = "".join(
            f"""
            <tr>
                <td class="sku">{p.sku}</td>
                <td>{p.nombre}</td>
                <td>{p.categoria.nombre}</td>
                <td>${p.precio}</td>
                <td>{p.stock_actual}</td>
                <td><span class="{
                    'badge-critico'
                    if p.stock_actual <= p.stock_minimo
                    else 'badge-optimo'
                }">
                    {
                        'Crítico'
                        if p.stock_actual <= p.stock_minimo
                        else 'Óptimo'
                    }
                </span></td>
                <td>
                    <form
                        method="POST"
                        action="?pestaana=tablero&usuario={usuario_activo}"
                    >
                        <input
                            type="hidden"
                            name="accion"
                            value="eliminar_producto"
                        >
                        <input
                            type="hidden"
                            name="sku_a_borrar"
                            value="{p.sku}"
                        >
                        <button
                            type="submit"
                            class="btn-danger"
                        >Eliminar</button>
                    </form>
                </td>
            </tr>
            """
            for p in productos_db
        )
        contenido_pantalla = f"""
        {error_bloque}
        <div class="card">
            <div class="card-header">
                <div><h1>📊 Inventario Retail</h1><div class="subtitle">
                    Existencias y alertas de stock.</div></div>
                <a
                    href="?pestaana=registro&usuario={usuario_activo}"
                    class="btn"
                >➕ Nuevo producto</a>
            </div>
            <div class="table-container">
                <table><thead><tr><th>SKU</th><th>Producto</th>
                <th>Categoría</th>
                <th>Precio</th><th>Stock</th><th>Estado</th><th>Acciones</th></tr></thead>
                <tbody>{
                    filas_productos or
                    '<tr><td colspan="7">No hay productos registrados.</td>'
                    '</tr>'
                }</tbody></table>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Inventario Retail</title>
    {estilos}</head>
    <body>
        <nav><div class="nav-brand">Inventario Retail</div>
            <div class="nav-links">
                <a
                    href="?pestaana=tablero&usuario={usuario_activo}"
                >Tablero</a>
                <a
                    href="?pestaana=registro&usuario={usuario_activo}"
                >Registrar</a>
                <a
                    href="?pestaana=movimientos&usuario={usuario_activo}"
                >Movimientos</a>
                <span class="nav-user">{usuario_activo}</span>
                <a
                    class="btn-switch"
                    href="?pestaana={pestaana}&usuario={siguiente_usuario}"
                >Cambiar usuario</a>
            </div>
        </nav>
        <main>{contenido_pantalla}</main>
    </body>
    </html>
    """
    return HttpResponse(html)
