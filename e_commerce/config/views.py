from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from django.core.paginator import Paginator

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