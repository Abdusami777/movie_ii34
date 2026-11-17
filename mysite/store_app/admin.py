from django.contrib import admin
from .models import UserProfile, Category, SubCategory, Product, ProductImage, Review, Cart, CartItem

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)