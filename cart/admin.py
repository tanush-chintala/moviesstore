from django.contrib import admin
from .models import Order, Item
admin.site.register(Item)
admin.site.register(Order)