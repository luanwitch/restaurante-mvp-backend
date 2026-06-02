from django.db import models
from products.models import Product


class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('money', 'Dinheiro'),
        ('pix', 'Pix'),
        ('card', 'Cartão'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Venda #{self.id} - R$ {self.total}'


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'