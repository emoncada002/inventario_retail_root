from django.http import HttpResponse


def dashboard_retail(request):
    """
    Controlador de la Fase 2 que inyecta el HTML con estilos CSS directos
    para garantizar la correcta visualización de colores en computadoras
    de escritorio.
    """
    html_contenido = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Almacén Retail - Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; background-color:
            #f3f4f6; margin: 0; padding: 0; color: #1f2937; }
            nav { background-color: #1e3a8a; padding: 16px; box-shadow:
            0 4px 6px -1px rgba(0,0,0,0.1); color: white; display: flex;
            justify-content: space-between; items-center: center; }
            .nav-brand { font-size: 20px; font-weight: bold;
            display: flex; align-items: center; gap: 8px; }
            .nav-links { display: flex; gap: 24px; font-size: 14px;
            align-items: center; }
            .nav-user { color: #bfdbfe; border-left: 1px solid #1e40af;
            padding-left: 16px; }
            main { max-width: 1200px; margin: 32px auto; padding: 0 16px; }
            .card { background-color: white; padding: 24px; rounded-radius:
            8px; border: 1px solid #e5e7eb; box-shadow:
            0 1px 3px rgba(0,0,0,0.1); border-radius: 8px; }
            .card-header { display: flex; justify-content: space-between;
            align-items: center; margin-bottom: 24px; }
            h1 { font-size: 24px; font-weight: bold; color: #111827; margin: 0;
            }
            .subtitle { font-size: 14px; color: #6b7280; margin-top: 4px; }
            .btn { background-color: #2563eb; color: white; font-weight: 500;
            font-size: 14px; padding: 8px 16px; border: none; border-radius:
            4px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
            .btn:hover { background-color: #1d4ed8; }
            .alert { background-color: #fef2f2; border-left: 4px solid #ef4444;
            padding: 16px; border-radius: 0 4px 4px 0; margin-bottom: 24px;
            display:flex; gap: 12px; }
            .alert-title { font-size: 14px; font-weight: 600; color: #991b1b;
            margin: 0; }
            .alert-desc { font-size: 12px; color: #b91c1c; margin-top: 4px; }
            .table-container { overflow-x: auto; margin-top: 16px; }
            table { width: 100%; border-collapse: collapse; text-align: left;
            font-size: 14px; }
            th { background-color: #f9fafb; padding: 12px 24px; font-weight:
            600; color: #4b5563; border-bottom: 1px solid #e5e7eb; }
            td { padding: 16px 24px; border-bottom: 1px solid #e5e7eb; }
            tr:hover { background-color: #f9fafb; }
            .sku { font-family: monospace; font-weight: bold; color: #1d4ed8; }
            .badge-optimo { background-color: #d1fae5; color: #065f46; padding:
            4px 10px; border-radius: 9999px; font-size: 12px; font-weight:
            600; display: inline-block; }
            .badge-critico { background-color: #fee2e2; color: #991b1b;
            padding: 4px 10px; border-radius: 9999px; font-size: 12px;
            font-weight: 600; display: inline-block; }
            footer { background-color: white; border-top: 1px solid #e5e7eb;
            padding: 16px 0; margin-top: 48px; text-align: center; font-size:
            12px; color: #6b7280; }
        </style>
    </head>
    <body>

        <!-- Barra de Navegación -->
        <nav>
            <div class="nav-brand">
                <span>🛒</span>
                <span>RetailStock Control</span>
            </div>
            <div class="nav-links">
                <span style="font-weight: 500;">📋 Tablero General</span>
                <span style="color: #d1d5db;">📦 Movimientos de Stock</span>
                <span class="nav-user">Colaborador: E. Moncada - S. Salcedo
                </span>
            </div>
        </nav>

        <!-- Contenedor Principal -->
        <main>
            <div class="card">
                <div class="card-header">
                    <div>
                        <h1>📋 Panel de Control de Inventario Retail</h1>
                        <div class="subtitle">Monitoreo de existencias en
                        tiempo real optimizado para computadoras de escritorio
                        (Fase 2 - Patrón DAO).</div>
                    </div>
                    <button class="btn">➕ Registrar Nuevo Producto</button>
                </div>

                <!-- Alerta de Stock Bajo Simulada -->
                <div class="alert">
                    <span style="font-size: 18px;">⚠️</span>
                    <div>
                        <h3 class="alert-title">
                        ATENCIÓN: Productos en Niveles Críticos</h3>
                        <p class="alert-desc">
                        Gorra Ajustable Retail (SKU: PROD-003) - Solo
                        quedan 3 piezas en almacén. Requieres
                        reabastecimiento inmediato.</p>
                    </div>
                </div>

                <!-- Tabla Base de Datos Simulada mediante DAO -->
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
                                <td style="font-weight: 500;">
                                Playera Polo Basic</td>
                                <td>Ropa</td>
                                <td style="font-weight: 500; color: #374151;">
                                $299.00</td>
                                <td style="font-weight: 600;">45 pzas</td>
                                <td><span class="badge-optimo">🟢 Stock Óptimo
                                </span></td>
                            </tr>
                            <tr>
                                <td class="sku">PROD-002</td>
                                <td style="font-weight: 500;">
                                Tenis Running Sport</td>
                                <td>Calzado</td>
                                <td style="font-weight: 500; color: #374151;">
                                $1,249.00</td>
                                <td style="font-weight: 600;">12 pzas</td>
                                <td><span class="badge-optimo">🟢 Stock Óptimo
                                </span></td>
                            </tr>
                            <tr>
                                <td class="sku">PROD-003</td>
                                <td style="font-weight: 500;">
                                Gorra Ajustable Retail</td>
                                <td>Accesorios</td>
                                <td style="font-weight: 500; color: #374151;">
                                $180.00</td>
                                <td style="font-weight: 600;">3 pzas</td>
                                <td><span class="badge-critico">🔴 Crítico
                                </span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>

        <footer>
            &copy; 2026 Sistema de Gestión de Inventario Retail.
            Proyectos Web EBC Campus Toluca.
        </footer>
    </body>
    </html>
    """
    return HttpResponse(html_contenido)
