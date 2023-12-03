from django.contrib import admin
from .models import Beer, Review

# Registered models
admin.site.register(Beer)
admin.site.register(Review)