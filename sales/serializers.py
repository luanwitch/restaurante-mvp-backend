from rest_framework import serializers
from .models import Sale, SaleItem
from inventory.models import ProductIngredient

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )


    class Meta:
        model = SaleItem
        fields = [
            'id',
            'product',
            'product_name',
            'quantity',
            'unit_price',
            'subtotal',
        ]
        read_only_fields = ['unit_price', 'subtotal']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = [
            'id',
            'payment_method',
            'total',
            'created_at',
            'items',
        ]
        read_only_fields = ['total']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        sale = Sale.objects.create(**validated_data)

        total = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            unit_price = product.price
            subtotal = unit_price * quantity

            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )

            recipes = ProductIngredient.objects.filter(product=product)

            for recipe in recipes:
                ingredient = recipe.ingredient
                ingredient.current_stock -= recipe.quantity * quantity
                ingredient.save()

            total += subtotal

        sale.total = total
        sale.save()

        return sale