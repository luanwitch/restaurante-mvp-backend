from rest_framework import viewsets

from .models import Ingredient, ProductIngredient
from .serializers import IngredientSerializer, ProductIngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class ProductIngredientViewSet(viewsets.ModelViewSet):
    queryset = ProductIngredient.objects.all()
    serializer_class = ProductIngredientSerializer