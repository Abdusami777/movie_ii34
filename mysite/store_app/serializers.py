from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (UserProfile, Category, SubCategory, Product,
                     ProductImage, Review, Cart, CartItem)

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {'username': instance.username, 'email': instance.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {'username': instance.username, 'email': instance.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['password', 'is_superuser', 'is_staff', 'groups', 'user_permissions']


class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'Category_name', 'Category_image']


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product_image']


class ProductListSerializer(serializers.ModelSerializer):
    photo_product = ProductImageSerializer(read_only=True, many=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)
    get_count_people = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'subcategory', 'photo_product', 'average_rating', 'get_count_people']


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    subcategory_product = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name', 'subcategory_product']


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_sub = SubCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'Category_name', 'category_sub']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileNameSerializer(read_only=True)
    created_data = serializers.DateField(format='%d-%m-%Y', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'star', 'text', 'created_data']


class ProductDetailSerializer(serializers.ModelSerializer):
    photo_product = ProductImageSerializer(read_only=True, many=True)
    subcategory = SubCategoryListSerializer(read_only=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)
    get_count_people = serializers.IntegerField(read_only=True)
    product_review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'subcategory', 'description',
                  'created_data', 'product_type', 'article', 'video',
                  'photo_product', 'get_count_people', 'average_rating', 'product_review']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()