from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, ProductIngredientViewSet, StockEntryViewSet, StockMovementViewSet

#Registrando as rotas
router = DefaultRouter()

#Mas o Django não sabe em qual URL isso deve aparecer
#É como dizer ao DRF:
#"Quando alguém acessar /ingredients/, use a IngredientViewSet."
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"product-ingredients", ProductIngredientViewSet)
router.register(r"recipes", ProductIngredientViewSet, basename="recipes")
router.register(r'stock-entries', StockEntryViewSet)
router.register(r"stock-movements", StockMovementViewSet, basename="stock-movements")

urlpatterns = router.urls

