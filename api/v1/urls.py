from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'api/v1/users', MyUserViewSet, basename='users')

router.register(r'api/v1/cart-items', CartItemViewSet, basename='cart-items')
router.register(r'api/v1/wishlist-items', WishListItemViewSet, basename='wishlist-items')

router.register(r'api/v1/categories', CategoryViewSet, basename='categories')
router.register(r'api/v1/products', ProductViewSet, basename='products')

router.register(r'api/v1/orders', OrderViewSet, basename='orders')
 
urlpatterns = [
    #user_management
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/api-token-auth/', CustomObtainAuthToken.as_view(), name='api_token_auth'),

    #cart_management
    path('api/v1/cart/', UserCartView.as_view(), name='user\'s cart'),
    path('api/v1/wishlist/', UserWishListView.as_view(), name='user\'s wishlist'),
    
    #shop
    path('api/v1/search-products/', ProductListView.as_view(), name='product-list'),
    path('api/v1/products/bulk-create/', BulkProductCreateView.as_view(), name='bulk-create-product'),

    #review_management
    path('api/v1/products/<int:product_id>/reviews/', ProductReviewListCreateView.as_view(), name='product-reviews-list-create'),
    path('api/v1/reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('api/v1/reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),

    path('', include(router.urls)),
]