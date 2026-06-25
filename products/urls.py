from rest_framework.routers import DefaultRouter
from .views import  CategoryViewSet, ProductViewSet
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ProductStockMovementViewSet,
)


#Registrando as rotas
router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-stock-movements',  ProductStockMovementViewSet)

urlpatterns = router.urls