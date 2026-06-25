from rest_framework import serializers
from django.db import transaction
from products.models import ProductStockMovement

from .models import Sale, SaleItem
from inventory.models import ProductIngredient, StockMovement


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "subtotal",
        ]
        read_only_fields = ["unit_price", "subtotal"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "payment_method",
            "total",
            "created_at",
            "items",
        ]
        read_only_fields = ["total", "created_at"]

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")

        if not items_data:
            raise serializers.ValidationError({
                "error": "A venda precisa ter pelo menos um item."
            })

        # 1. Valida estoque
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            recipes = ProductIngredient.objects.filter(product=product)

            if recipes.exists():
                for recipe in recipes:
                    ingredient = recipe.ingredient
                    required_quantity = recipe.quantity * quantity

                    if ingredient.current_stock < required_quantity:
                        raise serializers.ValidationError({
                            "error": (
                                f"Estoque insuficiente para {ingredient.name}. "
                                f"Necessário: {required_quantity}, "
                                f"Disponível: {ingredient.current_stock}."
                            )
                        })
            else:
                if product.stock_quantity < quantity:
                    raise serializers.ValidationError({
                        "error": (
                            f"Estoque insuficiente para {product.name}. "
                            f"Disponível: {product.stock_quantity}."
                        )
                    })

        # 2. Cria a venda
        sale = Sale.objects.create(**validated_data)
        total = 0

        # 3. Cria itens e baixa estoque
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            unit_price = product.price
            subtotal = unit_price * quantity

            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal,
            )

            total += subtotal

            recipes = ProductIngredient.objects.filter(product=product)

            if recipes.exists():
                for recipe in recipes:
                    ingredient = recipe.ingredient
                    movement_quantity = recipe.quantity * quantity

                    ingredient.current_stock -= movement_quantity
                    ingredient.save()

                    StockMovement.objects.create(
                        ingredient=ingredient,
                        movement_type="out",
                        quantity=movement_quantity,
                        notes=f"Venda do produto {product.name}",
                    )
            else:
                product.stock_quantity -= quantity
                product.save()

                ProductStockMovement.objects.create(
                    product=product,
                    movement_type="out",
                    quantity=quantity,
                    notes=f"Venda #{sale.id}",
                )

        # 4. Atualiza total
        sale.total = total
        sale.save()

        return sale