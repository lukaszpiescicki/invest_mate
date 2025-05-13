from django.contrib import admin

from .models import Stock, StockOperation, StockPrice, UserStock

admin.site.register(UserStock)
admin.site.register(StockOperation)
admin.site.register(StockPrice)


class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "ticker", "name")


admin.site.register(Stock, StockAdmin)
