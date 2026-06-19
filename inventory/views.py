from rest_framework import viewsets
from django.db.models import F

from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Ingredient, ProductIngredient, StockEntry, StockMovement
from .serializers import (
    IngredientSerializer,
    ProductIngredientSerializer,
    StockEntrySerializer,
    StockMovementSerializer
)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        ingredients = Ingredient.objects.filter(
            current_stock__lte=F('minimum_stock')
        )

        serializer = self.get_serializer(
            ingredients,
            many=True
        )

        return Response(serializer.data)


class ProductIngredientViewSet(viewsets.ModelViewSet):
    queryset = ProductIngredient.objects.all()
    serializer_class = ProductIngredientSerializer

class StockEntryViewSet(viewsets.ModelViewSet):
    queryset = StockEntry.objects.all()
    serializer_class = StockEntrySerializer 

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all().order_by('-created_at')
    serializer_class = StockMovementSerializer