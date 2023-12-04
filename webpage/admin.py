from django.contrib import admin
from .models import Beer, Review, MyBeer, CartItem, Order
# Registered models
admin.site.register(Beer)
admin.site.register(Review)
admin.site.register(MyBeer)
admin.site.register(CartItem)
admin.site.register(Order)
