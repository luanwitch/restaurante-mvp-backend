from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sales.models import Sale

from sales.models import Sale, SaleItem
from expenses.models import Expense
from inventory.models import Ingredient, StockMovement


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_report(request):
    total_sales = Sale.objects.count()

    total_revenue = (
        Sale.objects.aggregate(total=Sum("total"))["total"] or 0
    )

    total_expenses = (
        Expense.objects.aggregate(total=Sum("amount"))["total"] or 0
    )

    net_profit = total_revenue - total_expenses

    average_ticket = 0
    if total_sales > 0:
        average_ticket = total_revenue / total_sales

    best_seller = (
        SaleItem.objects
        .values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")
        .first()
    )

    ingredients = [
        {
            "id": ingredient.id,
            "name": ingredient.name,
            "unit": ingredient.unit,
            "current_stock": ingredient.current_stock,
            "minimum_stock": ingredient.minimum_stock,
            "status": (
                "low_stock"
                if ingredient.current_stock <= ingredient.minimum_stock
                else "ok"
            ),
        }
        for ingredient in Ingredient.objects.filter(active=True)
    ]

    movements = [
        {
            "id": movement.id,
            "ingredient_name": movement.ingredient.name,
            "movement_type": movement.movement_type,
            "quantity": movement.quantity,
            "notes": movement.notes,
            "created_at": movement.created_at,
        }
        for movement in StockMovement.objects.order_by("-created_at")[:20]
    ]

    return Response({
        "summary": {
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "average_ticket": average_ticket,
            "best_seller": best_seller,
        },
        "ingredients": ingredients,
        "movements": movements,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sales_report(request):

    sales = Sale.objects.prefetch_related(
        "items__product"
    ).order_by("-created_at")

    data = []

    for sale in sales: 
        data.append({
            "id": sale.id,
            "payment_method": sale.payment_method,
            "total": sale.total,
            "created_at": sale.created_at,
            "items": [
                {
                    "id": item.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal,
                }
                for item in sale.items.all()
            ]

        })

        return Response(data)