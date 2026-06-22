from rest_framework import serializers
from .models import Sale, SaleItem
from inventory.models import ProductIngredient, StockMovement


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
        read_only_fields = ['total', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # Valida estoque antes de criar a venda
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            recipes = ProductIngredient.objects.filter(product=product)

            if not recipes.exists():
                raise serializers.ValidationError({
                    "error": f"O produto {product.name} não possui receita cadastrada."
                })

            for recipe in recipes:
                ingredient = recipe.ingredient
                required_quantity = recipe.quantity * quantity

                if ingredient.current_stock < required_quantity:
                    raise serializers.ValidationError({
                        "error": (
                            f"Estoque insuficiente para {ingredient.name}. "
                            f"Necessário: {required_quantity}, "
                            f"Disponível: {ingredient.current_stock}"
                        )
                    })

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
                movement_quantity = recipe.quantity * quantity

                ingredient.current_stock -= recipe.quantity * quantity
                ingredient.save()

                StockMovement.objects.create(
                    ingredient=ingredient,
                    movement_type='out',
                    quantity=movement_quantity,
                    notes=f"Venda do produto {product.name}"
                )

            total += subtotal

        sale.total = total
        sale.save()

        return sale