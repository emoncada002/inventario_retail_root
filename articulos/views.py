from django.http import HttpResponse


def dashboard_retail(request):
    """
    Controlador de contingencia de la Fase 2 que inyecta el HTML directo
    para asegurar la visualización inmediata en computadoras de escritorio.
    """
    html_contenido = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Almacén Retail - Dashboard</title>
        <script src="https://tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 font-sans leading-normal tracking-normal">

        <!-- Barra de Navegación -->
        <nav class="bg-blue-900 p-4 shadow-md">
            <div class="container mx-auto flex justify-between items-center">
                <div class="flex items-center space-x-2">
                    <span class="text-2xl">🛒</span>
                    <span class="text-white font-bold text-xl tracking-tight">
                    RetailStock Control</span>
                </div>
                <div class="flex items-center space-x-6 text-sm">
                    <span class="text-white font-medium">📋 Tablero General
                    </span>
                    <span class="text-white hover:text-blue-200
                    transition font-medium">📦 Movimientos de Stock</span>
                    <span class="text-blue-200 border-l border-blue-700 pl-4">
                    Colaborador: E. Moncada - S. Salcedo</span>
                </div>
            </div>
        </nav>

        <!-- Contenedor Principal -->
        <main class="container mx-auto px-4 py-8">
            <div class="bg-white p-6 rounded-lg shadow-sm
            border border-gray-200">
                <div class="flex flex-col md:flex-row justify-between
                items-start md:items-center mb-6">
                    <div>
                        <h1 class="text-2xl font-bold text-gray-800">
                        📋 Panel de Control de Inventario Retail</h1>
                        <p class="text-sm text-gray-500 mt-1">
                        Monitoreo de existencias en tiempo real optimizado
                        para computadoras de escritorio (Fase 2 - Patrón DAO).
                        </p>
                    </div>
                    <button class="bg-blue-600 hover:bg-blue-700 text-white
                    font-medium text-sm py-2 px-4 rounded shadow transition">
                        ➕ Registrar Nuevo Producto
                    </button>
                </div>

                <!-- Alerta de Stock Bajo Simulada -->
                <div class="mb-6 bg-red-50 border-l-4 border-red-500
                p-4 rounded-r-md">
                    <div class="flex">
                        <span class="text-red-500 mr-3">⚠️</span>
                        <div>
                            <h3 class="text-sm font-semibold text-red-800">
                            ATENCIÓN: Productos en Niveles Críticos</h3>
                            <p class="text-xs text-red-700 mt-1">
                            Gorra Ajustable Retail (SKU: PROD-003)
                            -Solo quedan 3 piezas en almacén.
                            Requiere reabastecimiento.</p>
                        </div>
                    </div>
                </div>

                <!-- Tabla Base de Datos Simulada mediante DAO -->
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 text-sm">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left font-semibold
                                text-gray-600 tracking-wider">Código SKU</th>
                                <th class="px-6 py-3 text-left font-semibold
                                text-gray-600 tracking-wider">Descripción del
                                Producto</th>
                                <th class="px-6 py-3 text-left font-semibold
                                text-gray-600 tracking-wider">Categoría</th>
                                <th class="px-6 py-3 text-left font-semibold
                                text-gray-600 tracking-wider">Precio Unitario
                                </th>
                                <th class="px-6 py-3 text-left font-semibold
                                text-gray-600 tracking-wider">Existencias</th>
                                <th class="px-6 py-3 text-left font-semibold
                                text-gray-600 tracking-wider">Estado Almacén
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr class="hover:bg-gray-50 transition">
                                <td class="px-6 py-4 whitespace-nowrap
                                font-mono font-bold text-blue-700">PROD-001
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap
                                font-medium text-gray-900">Playera Polo Basic
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap
                                text-gray-500">Ropa</td>
                                <td class="px-6 py-4 whitespace-nowrap
                                font-medium text-gray-700">$299.00</td>
                                <td class="px-6 py-4 whitespace-nowrap
                                text-gray-900 font-semibold">45 pzas</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2.5 py-1 inline-flex
                                    text-xs leading-5 font-semibold
                                    rounded-full bg-green-100 text-green-800">
                                    🟢 Stock Óptimo</span>
                                </td>
                            </tr>
                            <tr class="hover:bg-gray-50 transition">
                                <td class="px-6 py-4 whitespace-nowrap
                                font-mono font-bold text-blue-700">PROD-002
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap
                                font-medium text-gray-900">Tenis Running Sport
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap
                                text-gray-500">Calzado</td>
                                <td class="px-6 py-4 whitespace-nowrap
                                font-medium text-gray-700">$1,249.00</td>
                                <td class="px-6 py-4 whitespace-nowrap
                                text-gray-900 font-semibold">12 pzas</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2.5 py-1 inline-flex
                                    text-xs leading-5 font-semibold
                                    rounded-full bg-green-100 text-green-800">
                                    🟢 Stock Óptimo</span>
                                </td>
                            </tr>
                            <tr class="hover:bg-gray-50 transition">
                                <td class="px-6 py-4 whitespace-nowrap
                                font-mono font-bold text-blue-700">PROD-003
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap
                                font-medium text-gray-900">
                                Gorra Ajustable Retail
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap
                                text-gray-500">Accesorios</td>
                                <td class="px-6 py-4 whitespace-nowrap
                                font-medium text-gray-700">$180.00</td>
                                <td class="px-6 py-4 whitespace-nowrap
                                text-gray-900 font-semibold">3 pzas</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2.5 py-1 inline-flex
                                    text-xs leading-5 font-semibold
                                    rounded-full
                                    bg-red-100 text-red-800">🔴 Crítico</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>

        <footer class="bg-white border-t border-gray-200 py-4 mt-12
        text-center text-xs text-gray-500">
            &copy; 2026 Sistema de Gestión de Inventario Retail.
            Proyectos Web EBC Campus Toluca.
        </footer>
    </body>
    </html>
    """
    return HttpResponse(html_contenido)
