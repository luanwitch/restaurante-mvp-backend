from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone

from expenses.models import Expense
from sales.models import Sale, SaleItem


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):

    period = request.GET.get('period')

    today = timezone.localdate()
    month_start = today.replace(day=1)

    # Querysets para cards inteligentes
    today_sales_queryset = Sale.objects.filter(
        created_at__date=today
    )

    month_sales_queryset = Sale.objects.filter(
        created_at__date__gte=month_start
    )

    today_expenses_queryset = Expense.objects.filter(
        expense_date=today
    )

    month_expenses_queryset = Expense.objects.filter(
        expense_date__gte=month_start
    )

    start_date = None

    if period == 'today':
        start_date = today

    elif period == '7days':
        start_date = today - timedelta(days=7)

    elif period == '30days':
        start_date = today - timedelta(days=30)

    elif period == 'month':
        start_date = month_start

    # Querysets principais
    sales_queryset = Sale.objects.all()
    expenses_queryset = Expense.objects.all()

    if start_date:
        sales_queryset = sales_queryset.filter(
            created_at__date__gte=start_date
        )

        expenses_queryset = expenses_queryset.filter(
            expense_date__gte=start_date
        )

    # Totais principais
    total_sales = sales_queryset.count()

    total_revenue = (
        sales_queryset.aggregate(
            total=Sum('total')
        )['total'] or 0
    )

    total_expenses = (
        expenses_queryset.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )

    net_profit = total_revenue - total_expenses

    average_ticket = 0

    if total_sales > 0:
        average_ticket = total_revenue / total_sales

    # Produto mais vendido
    best_seller = (
        SaleItem.objects
        .filter(sale__in=sales_queryset)
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')
        .first()
    )

    # Cards inteligentes
    today_revenue = (
        today_sales_queryset.aggregate(
            total=Sum('total')
        )['total'] or 0
    )

    month_revenue = (
        month_sales_queryset.aggregate(
            total=Sum('total')
        )['total'] or 0
    )

    today_expenses_total = (
        today_expenses_queryset.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )

    month_expenses_total = (
        month_expenses_queryset.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )

    today_profit = today_revenue - today_expenses_total
    month_profit = month_revenue - month_expenses_total

    return Response({
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'average_ticket': average_ticket,
        'best_seller': best_seller,
        'total_expenses': total_expenses,
        'net_profit': net_profit,

        'today_revenue': today_revenue,
        'today_expenses': today_expenses_total,
        'today_profit': today_profit,

        'month_revenue': month_revenue,
        'month_expenses': month_expenses_total,
        'month_profit': month_profit,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_per_day(request):

    period = request.GET.get('period')

    today = timezone.localdate()

    start_date = None

    if period == 'today':
        start_date = today

    elif period == '7days':
        start_date = today - timedelta(days=7)

    elif period == '30days':
        start_date = today - timedelta(days=30)

    elif period == 'month':
        start_date = today.replace(day=1)

    sales_queryset = Sale.objects.all()

    if start_date:
        sales_queryset = sales_queryset.filter(
            created_at__date__gte=start_date
        )

    sales = (
        sales_queryset
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('total'))
        .order_by('day')
    )

    return Response(sales)