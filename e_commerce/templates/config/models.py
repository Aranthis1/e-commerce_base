from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Product(models.Model):
    
    CATEGORY_CHOICES = [
        ('ELEC', 'Electrónica y Tecnología'),
        ('ROPA', 'Ropa y Accesorios'),
        ('HOGAR', 'Hogar y Muebles'),
        ('DEPORTE', 'Deportes y Aire Libre'),
        ('JUEGOS', 'Juguetes y Videojuegos'),
        ('OTROS', 'Otros'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    description = models.TextField(verbose_name="Descripción", blank=True)
    
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,
        default='OTROS',
        verbose_name="Categoría"
    )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio"
    )
    
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Imagen del producto")

    def __str__(self):
        return self.name