from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import *
from .permissions import *

from review_management.models import ProductRating

#USER MANAGEMENT

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    
class MyUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom token authentication view to support email-based authentication.
    """
    def post(self, request, *args, **kwargs):
        # Use custom LoginSerializer (which expects 'email' and 'password')
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CART MANAGEMENT

class UserCartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.cart

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartOrderProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.pk
        return CartOrderProduct.objects.filter(cart__customer=user)

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)

    def perform_update(self, serializer):
        cart = self.request.user.cart
        serializer.save(cart=cart)

    def perform_destroy(self, instance):
        if instance.cart.customer.pk == self.request.user.pk:
            instance.delete()
        else:
            self.permission_denied(self.request)
    
    
class UserWishListView(generics.RetrieveAPIView):
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wishlist
    
class WishListItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishListOrderProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user.pk
        return WishListOrderProduct.objects.filter(wishlist__customer=user)

    def perform_create(self, serializer):
        serializer.save(wishlist=self.request.user.wishlist)

    def perform_update(self, serializer):
        wishlist = self.request.user.wishlist
        serializer.save(wishlist=wishlist)

    def perform_destroy(self, instance):
        if instance.wishlist.customer.pk == self.request.user.pk:
            instance.delete()
        else:
            self.permission_denied(self.request)

#SHOP

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        
        name = self.request.query_params.get('name', None)
        brand = self.request.query_params.get('brand', None)
        category = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        elif category:
            queryset = queryset.filter(category=category)
        elif brand:
            queryset = queryset.filter(brand__icontains=brand)
        elif min_price:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset

class BulkProductCreateView(APIView):
    permission_classes = [IsAdminUser] 
    http_method_names = ["post"]
    
    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({"error": "Expected a list of items."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductRequiredFieldsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

#ORDER MANAGEMENT

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

#REVIEW MANAGEMENT

class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_rating__product__id=product_id)

    def perform_create(self, serializer):
        product_rating = ProductRating.objects.get(product__id=self.kwargs['product_id'])
        serializer.save(user=self.request.user, product_rating=product_rating)

class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        old_rating = self.get_object().rating
        serializer.save()

        new_rating = serializer.instance.rating
        if old_rating != new_rating:
            serializer.instance.product_rating.update_rating(old_rating, increase=False)
            serializer.instance.product_rating.update_rating(new_rating)

class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

