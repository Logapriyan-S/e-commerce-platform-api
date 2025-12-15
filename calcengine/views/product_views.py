from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Product, ProductImage
from ..serializers import ProductSerializer, ProductSuggestionSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        # Always set available=True on creation
        product = serializer.save(available=True)
        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

    def perform_update(self, serializer):
        product = serializer.save()
        images = self.request.FILES.getlist('images')
        if images:
            # Clear old images before adding new ones
            ProductImage.objects.filter(product=product).delete()
            for image in images:
                ProductImage.objects.create(product=product, image=image)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-created')  # removed available=True
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    filterset_fields = ['category__name']
    ordering_fields = ['name', 'price']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()  # removed available=True
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductSearchSuggestionsView(generics.ListAPIView):
    queryset = Product.objects.all()  # removed available=True
    serializer_class = ProductSuggestionSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset[:10]
