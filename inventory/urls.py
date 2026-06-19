from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, ProductIngredientViewSet, StockEntryViewSet

#Registrando as rotas
router = DefaultRouter()

#Mas o Django não sabe em qual URL isso deve aparecer
#É como dizer ao DRF:
#"Quando alguém acessar /ingredients/, use a IngredientViewSet."
router.register(
    r"ingredients",
    IngredientViewSet,
    basename="ingredients"
)

router.register(
    r"recipes",
    ProductIngredientViewSet,
    basename="recipes"
)

router.register(
    r'stock-entries',
    StockEntryViewSet
)

urlpatterns = router.urls

