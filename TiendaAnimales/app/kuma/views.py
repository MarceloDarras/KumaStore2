from django.shortcuts import render, redirect

from app.kuma.models import Categoria, Producto

import os

from django.conf import settings

# Create your views here.

def cargarInicio(request):
    productos = Producto.objects.all()
    return render(request, "inicio.html", {"prod": productos})
    
def cargarSesion(request):
   return render(request,"iniciosesion.html")

def cargarBandana(request):
    cate_bandanas = Producto.objects.filter(categoria_id = 4)
    return render(request, "bandanas.html", {"prod": cate_bandanas})

def cargarAgregarProducto(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, "agregar_producto.html", {"prod": productos, "cate": categorias})

def cargarCorreas(request):
    productos = Producto.objects.filter(categoria_id = 5)
    return render(request, "correas.html", {"prod": productos})

def cargarColgantes(request):
    productos = Producto.objects.filter(categoria_id = 6)
    return render(request, "identificadores.html", {"prod": productos})

def cargarJuguetes(request):
    productos = Producto.objects.filter(categoria_id = 7)
    return render(request, "juguetes.html", {"prod": productos})

def agregarProducto(request):
    #print("AGREGAR PRODUCTO", request.POST)
    v_sku = request.POST['txtSku']
    v_nombre = request.POST['txtNombre']
    v_descripcion = request.POST['txtDescripcion']
    v_precio = request.POST['txtPrecio']
    v_image = request.FILES['txtImg']
    if request.POST['fechaVencimientoSel'] == "":
        v_fecha_vencimiento = None
    else:
        v_fecha_vencimiento = request.POST['fechaVencimientoSel']
    v_stock = request.POST['txtStock']
    v_categoria = Categoria.objects.get(categoria_id = request.POST['cmdCategoria'])

    Producto.objects.create(sku = v_sku, nombre=v_nombre, descripcion=v_descripcion, stock=v_stock, precio=v_precio, fecha_vencimiento=v_fecha_vencimiento,categoria_id=v_categoria, imagen_url=v_image)

    return redirect('/agregarProducto')


def cargarEditarProductos(request, sku):
    productos= Producto.objects.get(sku = sku)
    categorias = Categoria.objects.all()

    cateId = productos.categoria_id

    productoCategoria = Categoria.objects.get(categoria_id = cateId.categoria_id).categoria_id

    return render(request, "editar_producto.html", {"prod": productos, "cate": categorias, "categoriaID": productoCategoria})

def editarProductoForm(request):
    v_id = request.POST['id']
    productoBD = Producto.objects.get(sku = v_id)
    v_nombre = request.POST['producto']
    v_descripcion = request.POST['descripcion']
    v_precio = request.POST['precio']
    v_fecha_vencimiento = request.POST['vencimiento']
    v_stock = request.POST['stock']
    v_categoria = Categoria.objects.get(categoria_id = request.POST['cmdCategoria'])

    try:
        v_image = request.FILE['imagen']
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(productoBD.imagen_url))
        os.remove(ruta_imagen)
    except:
        v_image = productoBD.imagen_url
    

    productoBD.nombre = v_nombre
    productoBD.descripcion = v_descripcion
    productoBD.stock = v_stock
    productoBD.precio = v_precio
    productoBD.fecha_vencimiento = v_fecha_vencimiento
    productoBD.imagen_url = v_image
    productoBD.categoria_id = v_categoria

    productoBD.save()


    return redirect('/agregar')

def eliminarProducto(request,sku):
    print("ELIMINAR PRODUCTO", sku)
    producto = Producto.objects.get(sku=sku)
    
    producto.delete()
    return redirect('/agregar')