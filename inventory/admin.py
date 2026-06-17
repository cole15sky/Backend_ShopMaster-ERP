from django.contrib import admin
from .models import Inventory, StockHistory

admin.site.register(Inventory)
admin.site.register(StockHistory)
