from django.urls import path
from .views import dashboard_summary, sales_per_day

urlpatterns = [
    path(
        'dashboard/summary/',
        dashboard_summary
    ),

    path(
        'dashboard/sales-per-day/', sales_per_day
    )
]