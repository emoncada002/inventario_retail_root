from django.http import HttpResponse


def dashboard_retail(request):
    """
    Controlador multi-pantalla y multi-usuario corregido.
    Integra formato dinámico 'f-string' y corrección de tamaño de botones.
    """
    pestaana = request.GET.get('pestaana', 'tablero')
    usuario_activo = request.GET.get('usuario', 'E. Moncada')
    siguiente_usuario = (
        "Sergio Salcedo" if usuario_activo == "E. Moncada" else "E. Moncada"
    )

    # BLOQUE DE ESTILOS COMPARTIDO
    estilos = """
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
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .nav-brand {{
            font-size: 20px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .nav-links {{
            display: flex;
            gap: 24px;
            font-size: 14px;
            align-items: center;
        }}
        .nav-links a {{
            color: white;
            text-decoration: none;
            font-weight: 500;
        }}
        .nav-links a:hover, .nav-links a.active {{
            color: #93c5fd;
            text-decoration: underline;
        }}
        .nav-user-block {{
            display: flex;
            align-items: center;
            gap: 12px;
            border-left: 1px solid #1e40af;
            padding-left: 16px;
        }}
        .nav-user {{ color: #bfdbfe; font-weight: 500; }}
        .btn-switch {{
            background-color: #2563eb;
            color: white;
            font-size: 13px;
            padding: 6px 12px;
            border: 1px solid #60a5fa;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
        }}
        .btn-switch:hover {{ background-color: #1d4ed8; }}
        main {{ max-width: 1200px; margin: 32px auto; padding: 0 16px; }}
        .card {{
            background-color: white;
            padding: 24px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }}
        h1 {{ font-size: 24px; font-weight: bold; color: #111827; margin: 0; }}
        .subtitle {{ font-size: 14px; color: #6b7280; margin-top: 4px; }}

        /* Corrección de tamaño fijo del botón de registro */
        .btn {{
            background-color: #2563eb;
            color: white;
            font-weight: 500;
            font-size: 14px;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            height: auto;
            line-height: normal;
        }}
        .btn:hover {{ background-color: #1d4ed8; }}

        .alert {{
            background-color: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 16px;
            border-radius: 0 4px 4px 0;
            margin-bottom: 24px;
            display: flex;
            gap: 12px;
        }}
        .alert-title {{
            font-size: 14px; font-weight: 600; color: #991b1b; margin: 0;
        }}
        .alert-desc {{ font-size: 12px; color: #b91c1c; margin-top: 4px; }}
        .table-container {{ overflow-x: auto; margin-top: 16px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left;
            font-size: 14px; }}
        th {{
            background-color: #f9fafb;
            padding: 12px 24px;
            font-weight: 600;
            color: #4b5563;
            border-bottom: 1px solid #e5e7eb;
        }}
        td {{ padding: 16px 24px; border-bottom: 1px solid #e5e7eb; }}
        tr:hover {{ background-color: #f9fafb; }}
        .sku {{ font-family: monospace; font-weight: bold; color: #1d4ed8; }}
        .badge-optimo {{
            background-color: #d1fae5; color: #065f46; padding: 4px 10px;
            border-radius: 9999px; font-size: 12px; font-weight: 600;
        }}
        .badge-critico {{
            background-color: #fee2e2; color: #991b1b; padding: 4px 10px;
            border-radius: 9999px; font-size: 12px; font-weight: 600;
        }}
        .form-group {{
            margin-bottom: 16px; display: flex; flex-direction: column;
            gap: 6px;
        }}
        .form-group label {{
            font-size: 14px; font-weight: 600; color: #374151;
        }}
        .form-group input, .form-group select {{
            padding: 10px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 14px;
        }}
        footer {{
            background-color: white; border-top: 1px solid #e5e7eb;
            padding: 16px 0; margin-top: 48px; text-align: center;
            font-size: 12px; color: #6b7280;
        }}
    </style>
    """

    estilos = estilos.replace('{{', '{').replace('}}', '}')

    contenido_pantalla = ""

    if pestaana == 'registro':
        contenido_pantalla = f"""
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
                >⬅️ Volver al Tablero</a>
            </div>
            <form style="max-width: 600px; margin-top: 24px;">
                <div class="form-group">
                    <label>Código SKU Universal:</label>
                    <input type="text" placeholder="Ej. PROD-004" required>
                </div>
                <div class="form-group">
                    <label>Descripción / Nombre del Artículo:</label>
                    <input
                        type="text"
                        placeholder="Ej. Mochila Ejecutiva"
                        required
                    >
                </div>
                <div class="form-group">
                    <label>Categoría Logística:</label>
                    <select>
                        <option>Ropa</option>
                        <option>Calzado</option>
                        <option>Accesorios</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Precio Unitario de Venta ($):</label>
                    <input
                        type="number"
                        step="0.01"
                        placeholder="0.00"
                        required
                    >
                </div>
                <div class="form-group">
                    <label>Existencias Iniciales en Almacén:</label>
                    <input
                        type="number"
                        placeholder="Cantidad de piezas"
                        required
                    >
                </div>
                <button
                    type="button"
                    class="btn"
                    onclick="
                        alert(
                            'Simulación CRUD: Guardado por {usuario_activo}'
                        );
                        window.location.href=
                            '?pestaana=tablero&usuario={usuario_activo}'
                    "
                    style="margin-top: 12px; width: 100%;"
                >💾 Guardar Producto</button>
            </form>
        </div>
        """
    elif pestaana == 'movimientos':
        contenido_pantalla = f"""
        <div class="card">
            <div class="card-header">
                <div>
                    <h1>📦 Registro de Movimientos de Almacén</h1>
                    <div class="subtitle">
                        Bitácora de flujos logísticos procesada por
                        {usuario_activo}.
                    </div>
                </div>
            </div>
            <form
                style="max-width: 600px; margin: 24px 0; padding-bottom: 24px;
                border-bottom: 1px solid #e5e7eb;"
            >
                <div class="form-group">
                    <label>Seleccionar Artículo:</label>
                    <select>
                        <option>PROD-001 - Playera Polo</option>
                        <option>PROD-002 - Tenis Running</option>
                        <option>PROD-003 - Gorra Ajustable</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Tipo de Flujo:</label>
                    <select>
                        <option>🔺 Entrada (Abastecimiento)</option>
                        <option>🔻 Salida (Venta)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Cantidad de Unidades:</label>
                    <input type="number" placeholder="Piezas a mover" required>
                </div>
                <button
                    type="button"
                    class="btn"
                    onclick="
                        alert('Movimiento registrado por {usuario_activo}');
                        window.location.href=
                            '?pestaana=tablero&usuario={usuario_activo}'
                    "
                    style="width: 100%;"
                >⚡ Procesar Movimiento</button>
            </form>
        </div>
        """
    else:
        contenido_pantalla = f"""
        <div class="card">
            <div class="card-header">
                <div>
                    <h1>📋 Panel de Inventario Retail</h1>
                    <div class="subtitle">
                        Monitoreo de existencias en tiempo real
                        (Fase 2 - Patrón DAO).
                    </div>
                </div>
                <div>
                    <a
                        href="?pestaana=registro&usuario={usuario_activo}"
                        class="btn"
                    >
                        ➕ Registrar Producto
                    </a>
                </div>
            </div>

            <div class="alert">
                <span style="font-size: 18px;">⚠️</span>
                <div>
                    <h3 class="alert-title">
                        ATENCIÓN: Productos en Niveles Críticos
                    </h3>
                    <p class="alert-desc">
                        Gorra Ajustable Retail (SKU: PROD-003): stock crítico.
                        Solo quedan 3 pzas.
                    </p>
                </div>
            </div>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>SKU</th><th>Producto</th>
                            <th>Existencias</th><th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="sku">PROD-001</td>
                            <td>Playera Polo Basic</td><td>45 pzas</td>
                            <td><span class="badge-optimo">🟢 Óptimo</span></td>
                        </tr>
                        <tr>
                            <td class="sku">PROD-002</td>
                            <td>Tenis Running Sport</td><td>12 pzas</td>
                            <td><span class="badge-optimo">🟢 Óptimo</span></td>
                        </tr>
                        <tr>
                            <td class="sku">PROD-003</td>
                            <td>Gorra Ajustable Retail</td><td>3 pzas</td>
                            <td>
                                <span class="badge-critico">
                                    🔴 Crítico
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """

    url_tablero = f"?pestaana=tablero&usuario={usuario_activo}"
    url_movimientos = f"?pestaana=movimientos&usuario={usuario_activo}"
    url_cambiar_usuario = f"?pestaana={pestaana}&usuario={siguiente_usuario}"
    clase_tablero = "active" if pestaana == "tablero" else ""
    clase_movimientos = "active" if pestaana == "movimientos" else ""

    # NOTA: Agregamos la letra 'f' aquí abajo antes de las
    # comillas para activar las variables dinámicas.
    html_final = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>RetailStock Control</title>
        {estilos}
    </head>
    <body>
        <nav>
            <div class="nav-brand">
                <span>📦</span>
                <span>Inventario Retail</span>
            </div>
            <div class="nav-links">
                <a
                    href="{url_tablero}"
                    class="{clase_tablero}"
                >Tablero</a>
                <a
                    href="{url_movimientos}"
                    class="{clase_movimientos}"
                >Movimientos</a>
                <div class="nav-user-block">
                    <span class="nav-user">👤 {usuario_activo}</span>
                    <a
                        href="{url_cambiar_usuario}"
                        class="btn-switch"
                    >Cambiar usuario</a>
                </div>
            </div>
        </nav>
        <main>
            {contenido_pantalla}
        </main>
        <footer>RetailStock Control · Gestión de inventario retail</footer>
    </body>
    </html>
    """

    return HttpResponse(html_final)
