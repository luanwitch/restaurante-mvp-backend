from rest_framework.viewsets import ModelViewSet
from .models import Sale
from .serializers import SaleSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all().order_by('-created_at')
    serializer_class = SaleSerializer
    permission_classes =  [IsAuthenticated]

    