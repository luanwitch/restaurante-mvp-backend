from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    name = models.CharField(
        max_length=100,
        unique=True
    )
    

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_quantity = models.PositiveBigIntegerField(
        default=0
    )

    min_stock = models.PositiveSmallIntegerField(
        default = 5
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

class ProductStockMovement(models.Model):
    MOVEMENT_TYPES = [
        ("in", "Entrada"),
        ("out", "Saída"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_movements"
    )

    movement_type = models.CharField(
        max_length=10,
        choices=MOVEMENT_TYPES
    )

    quantity = models.PositiveIntegerField()

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} - {self.quantity}"    