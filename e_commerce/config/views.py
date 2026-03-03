from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from django.contrib import messages
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from django.core.paginator import Paginator
from decimal import Decimal

def index(request):
    return render(request, 'index.html')

# /products/ (Listado)
def product_list(request):
    query = request.GET.get('q', '')
    products_list = Product.objects.all().order_by('-id')
    if query:
        products = products.filter(name__icontains=query)
    # --- CONFIGURACIÓN DE LA PAGINACIÓN ---
    # Dividimos la lista en páginas de 5 productos cada una
    paginator = Paginator(products_list, 5) 
    
    # Capturamos el número de página actual desde la URL (ej: ?page=2)
    page_number = request.GET.get('page')
    
    # Obtenemos solo los productos de esa página
    products = paginator.get_page(page_number)
    return render(request, 'products/product_list.html', {'products': products, 'query': query})

# /products/create/ (Creación)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto creado exitosamente!')
            return redirect('product_list')
        else:
            messages.error(request, 'Hubo un error al crear el producto. Por favor, revisa los campos.')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Crear'})

# /products/edit/<id>/ (Edición)
def product_edit(request, id):
    product = get_object_or_404(Product, id=id) # Falla con 404 si no existe
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto actualizado exitosamente!')
            return redirect('product_list')
        else:
            messages.error(request, 'Hubo un error al actualizar el producto. Por favor, revisa los campos.')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Editar'})

# /products/delete/<id>/ (Eliminación)
def product_delete(request, id):
    product = get_object_or_404(Product, id=id) # Falla con 404 si no existe
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado del catálogo.')
        return redirect('product_list')
        
    return render(request, 'products/product_confirm_delete.html', {'product': product})

# Esta vista es pública, no lleva @login_required
def public_catalog(request):
    query = request.GET.get('q', '')
    
    # Traemos todos los productos (puedes filtrar para que solo muestre los que tienen stock > 0)
    products_list = Product.objects.filter(stock__gt=0).order_by('-id')
    
    if query:
        products_list = products_list.filter(name__icontains=query)
        
    # Usamos el mismo paginador, pero mostramos 8 productos por página para la grilla
    paginator = Paginator(products_list, 8) 
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'public_catalog.html', {
        'products': products,
        'query': query
    })

from django.shortcuts import get_object_or_404, redirect
from .cart import Cart  # Importamos nuestro nuevo cerebro del carrito

# ... tus otras vistas ...

def cart_add(request, product_id):
    # 1. Creamos el objeto carrito pasándole la sesión actual
    cart = Cart(request)
    
    # 2. Buscamos el producto en la base de datos (o damos 404 si no existe)
    product = get_object_or_404(Product, id=product_id)
    
    # 3. Usamos la función 'add' que creamos en el paso 1
    cart.add(product=product)
    
    print("--- REPORTE DEL CARRITO ---")
    print(request.session.get('cart'))
    print("---------------------------")
    
    # 4. Redirigimos al usuario de vuelta a la tienda
    return redirect('public_catalog')

def cart_detail(request):
    # Traemos el carrito de la sesión (si no hay, traemos un diccionario vacío)
    session_cart = request.session.get('cart', {})
    
    cart_items = []
    cart_total = Decimal('0.00')
    
    # Recorremos lo que hay en la memoria
    for product_id, item_data in session_cart.items():
        # Buscamos el producto real en la base de datos
        product = Product.objects.get(id=product_id)
        
        # Calculamos el subtotal de ese producto (precio * cantidad)
        total_price = Decimal(item_data['price']) * item_data['quantity']
        cart_total += total_price
        
        # Armamos una lista con los datos listos para el HTML
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity'],
            'price': item_data['price'],
            'total_price': total_price
        })
        
    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })
def cart_remove(request, product_id):
    # 1. Llamamos al carrito actual
    cart = Cart(request)
    
    # 2. Buscamos el producto que el usuario quiere eliminar
    product = get_object_or_404(Product, id=product_id)
    
    # 3. Usamos la nueva función 'remove' que acabamos de crear
    cart.remove(product)
    
    # 4. Lo devolvemos a la pantalla del resumen de compra
    return redirect('cart_detail')
def cart_decrement(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Usamos la nueva función para restar
    cart.decrement(product)
    
    # Redirigimos de vuelta al resumen de compra
    return redirect('cart_detail')