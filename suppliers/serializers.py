from rest_framework import serializers
from .models import Supplier 

class SupplierSerializer(serializers.ModelSerializer):

    def validate_document(self, value):
        digits = ''.join(filter(str.isdigit, value))

        if len(digits) not in [11, 14]:
            raise self.serializers.ValidationErros(
                "CPF ou CNPJ inválido."
            )
        
        return value 
    
    class Meta:
        model = Supplier
        fields = '__all__'