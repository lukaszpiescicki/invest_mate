from django.urls import path

from .views import StockBuySellView, StockDetailView, StockListView

urlpatterns = [
    path("stocks/", StockListView.as_view(), name="stock-list"),
    path("stocks/<str:ticker>/", StockDetailView.as_view(), name="stock-detail"),
    path(
        "stocks/<int:stock_id>/transaction",
        StockBuySellView.as_view(),
        name="stock-transaction",
    ),
]
