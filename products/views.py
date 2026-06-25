from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from .models import Category, Product, ProductStockMovement
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductStockMovementSerializer,
)



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [SearchFilter]
    search_fields = ["name"]

    @action(detail=True, methods=["post"])
    def add_stock(self, request, pk=None):
        product = self.get_object()

        quantity = request.data.get("quantity")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"error": "Quantidade inválida."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity <= 0:
            return Response(
                {"error": "A quantidade deve ser maior que zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product.stock_quantity += quantity
        product.save()

        ProductStockMovement.objects.create(
            product=product,
            movement_type="in",
            quantity=quantity,
            notes="Entrada manual de estoque",
        )

        return Response({
            "message": "Estoque atualizado com sucesso.",
            "stock_quantity": product.stock_quantity,
        })
    
class ProductStockMovementViewSet(ModelViewSet):
    queryset = ProductStockMovement.objects.select_related(
        "product"
    ).order_by("-created_at")
    serializer_class = ProductStockMovementSerializer
    permission_classes = [IsAdminUser]    