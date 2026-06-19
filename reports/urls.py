from django.urls import path
from .views import dashboard_report, sales_report

urlpatterns = [
    path("reports/dashboard/", dashboard_report),
    path("reports/sales/", sales_report),
]