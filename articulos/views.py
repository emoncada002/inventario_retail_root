from django.http import HttpResponse


def dashboard_retail(request):
    """
    Controlador multi-pantalla que gestiona el Tablero, Registro y Movimientos
    basado en parámetros dinámicos de URL (?pestaana=...)
    """
    # Detectamos qué pestaña quiere ver el usuario (Por defecto es 'tablero')
    pestaana = request.GET.get('pestaana', 'tablero')

    # 1. BLOQUE DE ESTILOS COMPARTIDO
    estilos = """
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f4f6;
        margin: 0; padding: 0; color: #1f2937; }
        nav { background-color: #1e3a8a; padding: 16px; box-shadow:
        0 4px 6px rgba(0,0,0,0.1); color: white; display: flex;
        justify-content: space-between; align-items: center; }
        .nav-brand { font-size: 20px; font-weight: bold; display: flex;
        align-items: center; gap: 8px; }
        .nav-links { display: flex; gap: 24px; font-size: 14px;
        align-items: center; }
        .nav-links a { color: white; text-decoration: none; font-weight: 500; }
        .nav-links a:hover, .nav-links a.active { color: #93c5fd;
        text-decoration: underline; }
        .nav-user { color: #bfdbfe; border-left: 1px solid #1e40af;
        padding-left: 16px; }
        main { max-width: 1200px; margin: 32px auto; padding: 0 16px; }
        .card { background-color: white; padding: 24px; border:
        1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-radius: 8px; }
        .card-header { display: flex; justify-content: space-between;
        align-items: center; margin-bottom: 24px; }
        h1 { font-size: 24px; font-weight: bold; color: #111827; margin: 0; }
        .subtitle { font-size: 14px; color: #6b7280; margin-top: 4px; }
        .btn { background-color: #2563eb; color: white; font-weight: 500;
        font-size: 14px; padding: 8px 16px; border: none; border-radius: 4px;
        cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background-color: #1d4ed8; }
        .alert { background-color: #fef2f2; border-left: 4px solid #ef4444;
        padding: 16px; border-radius: 0 4px 4px 0; margin-bottom: 24px;
        display: flex; gap: 12px; }
        .alert-title { font-size: 14px; font-weight: 600; color: #991b1b;
        margin: 0; }
        .alert-desc { font-size: 12px; color: #b91c1c; margin-top: 4px; }
        .table-container { overflow-x: auto; margin-top: 16px; }
        table { width: 100%; border-collapse: collapse; text-align: left;
        font-size: 14px; }
        th { background-color: #f9fafb; padding: 12px 24px; font-weight: 600;
        color: #4b5563; border-bottom: 1px solid #e5e7eb; }
        td { padding: 16px 24px; border-bottom: 1px solid #e5e7eb; }
        tr:hover { background-color: #f9fafb; }
        .sku { font-family: monospace; font-weight: bold; color: #1d4ed8; }
        .badge-optimo { background-color: #d1fae5; color: #065f46;
        padding: 4px 10px; border-radius: 9999px; font-size: 12px;
        font-weight: 600; }
        .badge-critico { background-color: #fee2e2; color: #991b1b;
        padding: 4px 10px; border-radius: 9999px; font-size: 12px;
        font-weight: 600; }
        .form-group { margin-bottom: 16px; display: flex;
        flex-direction: column; gap: 6px; }
        .form-group label { font-size: 14px; font-weight: 600; color: #374151;
        }
        .form-group input, .form-group select { padding: 10px;
        border: 1px solid #d1d5db; border-radius: 4px; font-size: 14px; }
        footer { background-color: white; border-top: 1px solid #e5e7eb;
        padding: 16px 0; margin-top: 48px; text-align: center;
        font-size: 12px; color: #6b7280; }
    </style>
    """

    # 2. SELECCIÓN DE PANTALLA DINÁMICA
    contenido_pantalla = ""

    if pestaana == 'registro':
        # --- PANTALLA A: REGISTRO DE NUEVO PRODUCTO ---
        contenido_pantalla = """
        <div class="card">
            <div class="card-header">
                <div>
                    <h1>➕ Registrar Nuevo Producto de Retail</h1>
                    <div class="subtitle">Asignación de claves SKU y
                    existencias iniciales (Fase 2 - Formulario CRUD).
                    </div>
                </div>
                <a href="?pestaana=tablero" class="btn"
                style="background-color: #4b5563;">⬅️ Volver al Tablero</a>
            </div>
            <form style="max-width: 600px; margin-top: 24px;">
                <div class="form-group">
                    <label>Código SKU Universal:</label>
                    <input type="text" placeholder="Ej. PROD-004" required>
                </div>
                <div class="form-group">
                    <label>Descripción / Nombre del Artículo:</label>
                    <input type="text" placeholder="Ej.
                    Mochila Ejecutiva Impermeable" required>
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
                    <input type="number" step="0.01"
                    placeholder="0.00" required>
                </div>
                <div class="form-group">
                    <label>Existencias Iniciales en Almacén:</label>
                    <input type="number" placeholder=
                    "Cantidad de piezas iniciales" required>
                </div>
                <button type="button" class="btn" onclick=
                "alert('Simulación CRUD: Producto guardado a través
                de InventarioDAO'); window.location.href='?pestaana=tablero'"
                style="margin-top: 12px; width: 100%;">💾 Guardar Producto
                en Almacén</button>
            </form>
        </div>
        """
    elif pestaana == 'movimientos':
        # --- PANTALLA B: MOVIMIENTOS DE STOCK ---
        contenido_pantalla = """
        <div class="card">
            <div class="card-header">
                <div>
                    <h1>📦 Registro de Movimientos de Almacén</h1>
                    <div class="subtitle">Bitácora lógica de entradas y
                    salidas de mercancía minorista.</div>
                </div>
            </div>
            <form style="max-width: 600px; margin: 24px 0;
            padding-bottom: 24px; border-bottom: 1px solid #e5e7eb;">
                <div class="form-group">
                    <label>Seleccionar Artículo afectado:</label>
                    <select>
                        <option>PROD-001 - Playera Polo Basic
                        (Stock actual: 45)</option>
                        <option>PROD-002 - Tenis Running Sport
                        (Stock actual: 12)</option>
                        <option>PROD-003 - Gorra Ajustable Retail
                        (Stock actual: 3)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Tipo de Flujo Físico:</label>
                    <select>
                        <option>🔺 Entrada (Abastecimiento de Proveedor)
                        </option>
                        <option>🔻 Salida (Venta / Merma de Inventario)
                        </option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Cantidad de Unidades:</label>
                    <input type="number" placeholder=
                    "Cantidad de piezas a mover" required>
                </div>
                <button type="button" class="btn" onclick="alert
                ('Movimiento registrado en la bitácora física');
                window.location.href='?pestaana=tablero'"
                style="width: 100%;">⚡ Procesar Movimiento de Almacén
                </button>
            </form>
            <h3>Historial de Auditoría Reciente</h3>
            <div class="table-container">
                <table>
                    <thead>
                        <tr><th>Fecha/Hora</th><th>SKU</th><th>Tipo</th><th>Cantidad</th><th>Responsable</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>20/Aug/2026 14:22</td><td class="sku">PROD-001
                        </td><td>Entrada</td><td>+10 pzas</td><td>E. Moncada
                        </td></tr>
                        <tr><td>20/Aug/2026 11:05</td><td class="sku">PROD-003
                        </td><td>Salida (Venta)</td><td>-2 pzas</td><td>
                        E. Moncada</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        """
    else:
        # --- PANTALLA C: TABLERO GENERAL (POR DEFECTO) ---
        contenido_pantalla = """
        <div class="card">
            <div class="card-header">
                <div>
                    <h1>📋 Panel de Control de Inventario Retail</h1>
                    <div class="subtitle">Monitoreo de existencias en tiempo
                    real optimizado para computadoras de escritorio
                    (Fase 2 - Patrón DAO).</div>
                </div>
                <a href="?pestaana=registro" class="btn">➕ Registrar
                Nuevo Producto</a>
            </div>

            <div class="alert">
                <span style="font-size: 18px;">⚠️</span>
                <div>
                    <h3 class="alert-title">ATENCIÓN:
                    Productos en Niveles Críticos</h3>
                    <p class="alert-desc">Gorra Ajustable Retail
                    (SKU: PROD-003) - Solo quedan 3 piezas en almacén.
                    Requieres reabastecimiento inmediato.</p>
                </div>
            </div>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Código SKU</th>
                            <th>Descripción del Producto</th>
                            <th>Categoría</th>
                            <th>Precio Unitario</th>
                            <th>Existencias</th>
                            <th>Estado Almacén</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="sku">PROD-001</td>
                            <td style="font-weight: 500;">Playera Polo Basic
                            </td>
                            <td>Ropa</td>
                            <td style="font-weight: 500; color: #374151;">
                            $299.00</td>
                            <td style="font-weight: 600;">45</td>
                            <td><span class="badge-optimo">Óptimo</span></td>
                        </tr>
                        <tr>
                            <td class="sku">PROD-002</td>
                            <td style="font-weight: 500;">Tenis Running Sport
                            </td>
                            <td>Calzado</td>
                            <td style="font-weight: 500; color: #374151;">
                            $1,299.00</td>
                            <td style="font-weight: 600;">12</td>
                            <td><span class="badge-optimo">Óptimo</span></td>
                        </tr>
                        <tr>
                            <td class="sku">PROD-003</td>
                            <td style="font-weight: 500;">
                            Gorra Ajustable Retail</td>
                            <td>Accesorios</td>
                            <td style="font-weight: 500; color: #374151;">
                            $199.00</td>
                            <td style="font-weight: 600;">3</td>
                            <td><span class="badge-critico">Crítico</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """

    # 3. NAVEGACIÓN PRINCIPAL + LAYOUT BASE
    respuesta = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inventario Retail</title>
        {estilos}
    </head>
    <body>
        <nav>
            <div class="nav-brand">🏬 Inventario Retail</div>
            <div class="nav-links">
                <a href="?pestaana=tablero"
                   class="{'active' if pestaana == 'tablero' else ''}">Tablero
                   </a>
                <a href="?pestaana=registro"
                   class="{'active' if pestaana == 'registro' else ''}">
                   Registro</a>
                <a href="?pestaana=movimientos"
                   class="{'active' if pestaana == 'movimientos' else ''}">
                   Movimientos</a>
            </div>
            <div class="nav-user">Usuario: E. Moncada</div>
        </nav>
        <main>
            {contenido_pantalla}
        </main>
        <footer>© 2026 Inventario Retail •
        Fase 2: Interfaz de control y monitoreo</footer>
    </body>
    </html>
    """

    return HttpResponse(respuesta)
