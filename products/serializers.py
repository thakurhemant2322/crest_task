from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','price','discount','image','ssn','is_active','created_on','updated_on']
        read_only_fields = ['is_active', 'created_on', 'updated_on']

class BulkProductSerializer(serializers.ListSerializer):
    child = ProductSerializer()
    allow_empty = False
