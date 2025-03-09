from django.contrib import admin

from .models import Stock, StockOperation, StockPrice, UserStock

admin.site.register(Stock)
admin.site.register(UserStock)
admin.site.register(StockOperation)
admin.site.register(StockPrice)
