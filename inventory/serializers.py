from rest_framework import serializers
from .models import Ingredient, ProductIngredient

class IngredientSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Ingredient
        fields = "__all__"


class ProductIngredientSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProductIngredient
        fields = "__all__"
