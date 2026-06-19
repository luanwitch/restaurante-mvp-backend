from rest_framework import serializers
from .models import Ingredient, ProductIngredient, StockEntry, StockMovement

class IngredientSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Ingredient
        fields = "__all__"


class ProductIngredientSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProductIngredient
        fields = "__all__"

class StockEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = StockEntry
        fields = "__all__"

    def create(self, validated_data):
        stock_entry = StockEntry.objects.create(
            **validated_data
        ) 

        ingredient = stock_entry.ingredient
        ingredient.current_stock += stock_entry.quantity 
        ingredient.save()  

        StockMovement.objects.create(
            ingredient = ingredient,
            movement_type='in',
            quantity=stock_entry.quantity,
            notes=stock_entry.notes
        )

        return stock_entry
    
class StockMovementSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )    

    class Meta:
        model = StockMovement
        fields = [
            'id',
            'ingredient',
            'ingredient_name',
            'movement_type',
            'quantity',
            'notes',
            'created_at',
        ]