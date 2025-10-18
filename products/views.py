from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.http import HttpResponse
from openpyxl import Workbook

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from .filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_scope = "products"
    filterset_class = ProductFilter
    search_fields = ['title','description']
    ordering_fields = ['created_on','updated_on','price']

    def get_queryset(self):
        qs = Product.objects.all()
        # Only active by default
        if self.request and self.request.query_params.get('include_inactive') != '1':
            qs = qs.filter(is_active=True)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_active:
            return Response({"detail": "Already inactive."}, status=status.HTTP_400_BAD_REQUEST)
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        product = self.get_object()
        if not product.is_active:
            return Response({'detail': 'Product already disabled.'}, status=400)
        product.is_active = False
        product.save(update_fields=['is_active'])
        return Response({'detail': 'Product disabled successfully.'})

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if not request.user.is_authenticated or not request.user.groups.filter(name='admin').exists():
            return Response({'detail': 'Admin only.'}, status=403)
        serializer = ProductSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer.validated_data)
        return Response({'detail': f"Created {len(serializer.validated_data)} products."}, status=201)

    def perform_bulk_create(self, items):
        objs = [Product(**item) for item in items]
        Product.objects.bulk_create(objs, ignore_conflicts=True)

class ExportProductsExcel(APIView):
    throttle_scope = "products"
    def get(self, request):
        qs = Product.objects.all()
        wb = Workbook()
        ws = wb.active
        ws.title = 'Products'
        ws.append(['ID','Title','Description','Price','Discount','Image','SSN','Is Active','Created On','Updated On'])
        for p in qs:
            ws.append([p.id, p.title, p.description, float(p.price), float(p.discount), p.image, p.ssn, p.is_active, p.created_on.isoformat(), p.updated_on.isoformat()])
        from io import BytesIO
        stream = BytesIO()
        wb.save(stream)
        resp = HttpResponse(stream.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        resp['Content-Disposition'] = 'attachment; filename=products.xlsx'
        return resp
