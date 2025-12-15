from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views.auth_views import MyLoginView, RegisterView, ProfileView
from .views.product_views import (
    ProductViewSet, ProductListView, ProductSearchSuggestionsView, ProductDetailView
)
from .views.category_views import CategoryViewSet
from .views.cart_views import CartViewSet
from .views.order_views import OrderViewSet

router = DefaultRouter()
router.register(r'admin/products', ProductViewSet, basename='product-admin')
router.register(r'admin/categories', CategoryViewSet, basename='category-admin')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Auth Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='user_profile'),

    # Public Product Endpoints
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/search-suggestions/', ProductSearchSuggestionsView.as_view(), name='product-search-suggestions'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'), # NEW: URL for a single product

    # Include router-generated URLs
    path('', include(router.urls)),
]