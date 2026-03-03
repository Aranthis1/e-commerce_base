from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self, request):
        """Inicializa el carrito pidiéndole la sesión a Django"""
        self.session = request.session
        # Intenta obtener el carrito actual
        cart = self.session.get('cart')
        
        # Si el usuario es nuevo y no tiene carrito, le creamos uno vacío {}
        if not cart:
            cart = self.session['cart'] = {}
            
        self.cart = cart

    def add(self, product, quantity=1):
        """Agrega un producto al carrito o actualiza su cantidad"""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
            
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Le avisa a Django que la sesión ha sido modificada y debe guardarse"""
        self.session.modified = True

    def clear(self):
        """Vacía el carrito por completo (útil para cuando el cliente ya pagó)"""
        del self.session['cart']
        self.save()

    def remove(self, product):
        """Elimina un producto por completo del carrito"""
        product_id = str(product.id)
        
        # Si el producto está en el carrito, lo borramos del diccionario
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        """Resta 1 a la cantidad del producto. Si llega a 0, lo elimina."""
        product_id = str(product.id)
        
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            
            # Si al restar la cantidad queda en 0 (o menos), lo borramos por completo
            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product)
            else:
                self.save()