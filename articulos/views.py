from django.shortcuts import render
from articulos.dao.inventariodao import InventarioDAO


def dashboard_retail(request):
    """
    Controlador principal que gestiona la pantalla de lectura general del
    inventario.
    """
    # Consumimos los datos a través de la capa intermedia del Patrón DAO
    inventario_completo = InventarioDAO.obtener_todo_el_inventario()
    alertas_criticas = InventarioDAO.consultar_alertas_stock_critico()

    contexto = {
        'productos': inventario_completo,
        'alertas': alertas_criticas,
        'titulo_modulo': (
            'Sistema de Gestión de Almacén - Retail'
        )
    }

    # Renderiza la interfaz utilizando la plantilla especializada
    # para el tablero
    return render(request, 'mainvista/tablero.html', contexto)
