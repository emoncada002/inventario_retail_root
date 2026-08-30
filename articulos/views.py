from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from articulos.dao.inventariodao import InventarioDAO
from articulos.models import Producto, Categoria
from django.contrib.auth.decorators import login_required, user_passes_test

# Roles


def es_admin(user):
    """Verifica si el usuario pertenece a 'Administración' o es staff"""
    return user.is_authenticated and (
        user.groups.filter(name='Administración').exists() or user.is_staff
    )
    # return user.is_authenticated and (
    #     user.groups.filter(name='Cocina').exists() or user.is_staff
    # )


@login_required
@user_passes_test(es_admin, login_url='/admin/login/')
@csrf_exempt
def dashboard_retail(request):
    """
    Controlador lógico definitivo de la Fase 3.
    Procesa las operaciones CRUD y delega la renderización visual
    al motor de plantillas nativo de Django.
    """
    pestaana = request.GET.get('pestaana', 'tablero')
    usuario_activo = request.GET.get('usuario', 'E. Moncada')
    siguiente_usuario = (
        "Sergio Salcedo" if usuario_activo == "E. Moncada" else "E. Moncada"
    )

    # Garantizar la existencia de categorías base en el catálogo logístico
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

    # PROCESAMIENTO DE PETICIONES POST (GUARDADO, ACTUALIZACIÓN Y BAJAS
    # DE REGISTROS)
    if request.method == "POST":
        accion = request.POST.get('accion')

        if accion == "guardar_producto":
            cat = Categoria.objects.get(nombre=request.POST.get('categoria'))
            nuevo_prod = InventarioDAO.insertar_nuevo_producto(
                sku=request.POST.get('sku'),
                nombre=request.POST.get('nombre'),
                categoria_id=cat.id,
                precio=request.POST.get('precio'),
                stock_inicial=request.POST.get('stock'),
                stock_min=5
            )
            if request.FILES.get('imagen_prod'):
                nuevo_prod.imagen = request.FILES.get('imagen_prod')
                nuevo_prod.save()
            return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")

        elif accion == "actualizar_producto":
            sku = request.POST.get('sku')
            prod = Producto.objects.get(sku=sku)
            cat = Categoria.objects.get(nombre=request.POST.get('categoria'))

            prod.nombre = request.POST.get('nombre')
            prod.categoria = cat
            prod.precio = request.POST.get('precio')
            prod.stock_actual = int(request.POST.get('stock'))

            if request.FILES.get('imagen_prod'):
                prod.imagen = request.FILES.get('imagen_prod')

            prod.save()
            return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")

        elif accion == "procesar_movimiento":
            prod = Producto.objects.get(sku=request.POST.get('sku_afectado'))
            cantidad = int(request.POST.get('cantidad', 0))
            if "Entrada" in request.POST.get('tipo_flujo'):
                prod.stock_actual += cantidad
            else:
                prod.stock_actual = max(0, prod.stock_actual - cantidad)
            prod.save()
            return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")

        elif accion == "eliminar_producto":
            prod = Producto.objects.get(sku=request.POST.get('sku_a_borrar'))
            prod.delete()
            return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")

    # EXTRACCIÓN DE DATOS REALES UTILIZANDO EL PATRÓN DAO
    productos_db = InventarioDAO.obtener_todo_el_inventario()
    alertas_db = InventarioDAO.consultar_alertas_stock_critico()

    # Preparamos el diccionario de contexto para las plantillas HTML
    contexto = {
        'pestaana': pestaana,
        'usuario_activo': usuario_activo,
        'siguiente_usuario': siguiente_usuario,
        'productos': productos_db,
        'alertas': alertas_db,
    }

    # SELECCIÓN Y RETORNO DE TEMPLATES SEGÚN LA PESTAÑA ACTIVA
    if pestaana == 'registro':
        return render(request, 'mainvista/almacen.html', contexto)
    elif pestaana == 'editar':
        sku_editar = request.GET.get('sku_editar')
        contexto['prod_a_editar'] = Producto.objects.get(sku=sku_editar)
        return render(request, 'mainvista/almacen.html', contexto)
    elif pestaana == 'movimientos':
        return render(request, 'mainvista/movimientos.html', contexto)

    # Renderización por defecto del Tablero General
    return render(request, 'mainvista/tablero.html', contexto)
