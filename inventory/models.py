from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    UNIT_CHOICES = [
        ("kg", "Quilograma"),
        ("g", "Grama"),
        ("l", "Litro"),
        ("ml", "Mililitro"),
        ("un", "Unidade"),
    ]

    #Limitar os valores permitidos, com o "choices" o Django so aceita: kg,g,l,ml,un.
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

    #Quantida atual em stock:
    current_stock = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0
    )

    #Quantidade mínima permitida
    minimum_stock = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class ProductIngredient(models.Model):    

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="recipe"
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT
        )
    
    quantity = models.DecimalField(
         max_digits=10,
         decimal_places=3
    )

    def __str__(self):
            return f"{self.product.name} - {self.ingredient.name}"

