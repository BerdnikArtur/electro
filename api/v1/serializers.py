from rest_framework import serializers

from shop.models import Product, Category
from user_management.models import CustomUser
from order_management.models import Order, BillingAddress
from cart_management.models import Cart, WishList, CartOrderProduct, WishListOrderProduct
from review_management.models import Review

#USER MANAGEMENT

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

#CART MANAGEMENT

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrderProduct
        exclude = ['cart']

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

class WishListOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListOrderProduct
        exclude = ['wishlist']

#SHOP 

class ProductRequiredFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['slug', 'count_of_selled', 'time_created', 'time_updated']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

#ORDER MANAGEMENT

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

#REVIEW MANAGEMENT

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'date_created', 'user', 'product_rating']
        read_only_fields = ['id', 'date_created', 'user', 'product_rating']

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review