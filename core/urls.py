from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from inventory.views import (
    IngredientViewSet,
    ProductIngredientViewSet,
    StockEntryViewSet,
    StockMovementViewSet,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'product-ingredients', ProductIngredientViewSet, basename='product-ingredient')
router.register(r'stock-movements', StockMovementViewSet, basename='stock-movement')
router.register(r'stock-entries', StockEntryViewSet, basename='stock-entry')

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("products.urls")),
    path("api/", include("sales.urls")),
    path("api/", include("dashboard.urls")),
    path("api/", include("expenses.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("customers.urls")),
    path("api/", include("suppliers.urls")),
    path("api/", include("inventory.urls")),
    path("api/", include("reports.urls")),

    path("api/", include(router.urls)),

    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    
]