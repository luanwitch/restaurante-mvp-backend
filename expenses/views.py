from rest_framework.viewsets import ModelViewSet
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all().order_by('-expense_date')
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]