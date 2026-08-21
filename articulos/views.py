from django.http import HttpResponse


def dashboard_retail(request):
    """Renderiza el tablero, el registro o los movimientos del inventario."""
    pestaana = request.GET.get("pestaana", "tablero")
    usuario_activo = request.GET.get("usuario", "E. Moncada")
    siguiente_usuario = (
        "Sergio Salcedo" if usuario_activo == "E. Moncada" else "E. Moncada"
    )

    estilos = """
    <style>
        body { font-family: Arial, sans-serif; background: #f3f4f6; margin: 0;
        color: #1f2937; }
        nav { background: #1e3a8a; padding: 16px; color: white; display: flex;
        justify-content: space-between; }
        .nav-links { display: flex; gap: 24px; align-items: center; }
        nav a { color: white; text-decoration: none; }
        main { max-width: 1200px; margin: 32px auto; padding: 0 16px; }
        .card { background: white; padding: 24px; border-radius: 8px; }
        .card-header { display: flex; justify-content: space-between;
        margin-bottom: 24px; }
        .btn { background: #2563eb; color: white; padding: 8px 16px;
        border: 0; border-radius: 4px; text-decoration: none; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 12px; border-bottom: 1px solid #e5e7eb; }
        .sku { font-family: monospace; font-weight: bold; color: #1d4ed8; }
        .badge-optimo { color: #065f46; } .badge-critico { color: #991b1b; }
        .form-group { margin-bottom: 16px; display: flex;
        flex-direction: column; gap: 6px; }
    </style>
    """

    if pestaana == "registro":
        contenido_pantalla = f"""
        <div class="card"><div class="card-header"><div><h1>
        ➕ Registrar Nuevo Producto</h1>
        <p>Operador: {usuario_activo}</p></div>
        <a class="btn" href="?pestaana=tablero&usuario={usuario_activo}">
        Volver</a></div>
        <form><div class="form-group"><label> Código SKU:</label>
        <input required></div>
        <div class="form-group"><label>Descripción:</label><input required>
        </div>
        <div class="form-group"><label>Precio:</label><input type="number"
        step="0.01" required></div>
        <div class="form-group"><label>Existencias:</label><input type="number"
        required></div>
        <button class="btn" type="button">💾 Guardar Producto</button></form>
        </div>"""
    elif pestaana == "movimientos":
        contenido_pantalla = """
        <div class="card"><h1>📦 Movimientos de Almacén</h1>
        <form><div class="form-group"><label>Artículo:</label><select><option>
        PROD-001 - Playera Polo Basic</option><option>PROD-002 - Tenis Running
        Sport</option></select></div>
        <div class="form-group"><label>Cantidad:</label><input type="number"
        required></div>
        <button class="btn" type="button">⚡ Procesar Movimiento</button></form>
        </div>"""
    else:
        contenido_pantalla = """
        <div class="card">
            <div class="card-header"><h1>📋 Panel de Inventario Retail</h1>
            <a class="btn" href="?pestaana=registro&usuario={usuario_activo}">
            ➕ Registrar Producto</a></div>
            <p>⚠️ Gorra Ajustable Retail (PROD-003): stock crítico.</p>
            <table><thead><tr><th>SKU</th><th>Producto</th><th>Existencias</th><th>Estado</th></tr></thead><tbody>
            <tr><td class="sku">PROD-001</td><td>Playera Polo Basic</td><td>
            45 pzas</td><td class="badge-optimo">🟢 Óptimo</td></tr>
            <tr><td class="sku">PROD-002</td><td>Tenis Running Sport</td>
            <td>12 pzas</td><td class="badge-optimo">🟢 Óptimo</td></tr>
            <tr><td class="sku">PROD-003</td><td>Gorra Ajustable Retail</td>
            <td>3 pzas</td><td class="badge-critico">🔴 Crítico</td></tr>
            </tbody></table></div>"""

    html = f"""
    <!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>
    Inventario Retail</title>{estilos}</head>
    <body><nav><strong>📦 Inventario Retail</strong><div class="nav-links">
    <a href="?pestaana=tablero&usuario={usuario_activo}">Tablero</a>
    <a href="?pestaana=movimientos&usuario={usuario_activo}">Movimientos</a>
    <span>👤 {usuario_activo}</span><a class="btn" href="?pestaana={pestaana}
    &usuario={siguiente_usuario}">Cambiar usuario</a>
    </div></nav><main>{contenido_pantalla}</main><footer>Inventario Retail —
    Fase 2</footer></body></html>
    """
    return HttpResponse(html)
