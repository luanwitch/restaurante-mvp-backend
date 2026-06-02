from django.contrib import admin
from django.urls import include, path 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('sales.urls')),
    path('api/', include('dashboard.urls')),
    path('api/', include('expenses.urls')),
    path('api/', include('dashboard.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/', include('accounts.urls')),
    path('api/', include('customers.urls')),
    path('api/', include('suppliers.urls')),
]
