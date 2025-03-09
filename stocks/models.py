from django.conf import settings
from django.db import models

from stock_market.models import StockMarket
from wallets.models import Wallet


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    market_cap = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    stock_market = models.ForeignKey(
        StockMarket, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    wallet = models.ManyToManyField(Wallet, blank=True)

    @property
    def get_last_prices(self):
        last_price = self.historical_prices.all().order_by("-date").first()
        if last_price:
            return {
                "date": last_price.date,
                "open_price": last_price.open_price,
                "close_price": last_price.close_price,
                "highest_price": last_price.highest_price,
                "lowest_price": last_price.lowest_price,
                "volume": last_price.volume,
            }
        return None


class UserStock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    total_quantity = models.PositiveIntegerField(default=0)
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    average_purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.user} owns {self.total_quantity} shares of {self.stock.ticker}"


class StockOperation(models.Model):
    user_stock = models.ForeignKey(
        UserStock, on_delete=models.CASCADE, related_name="purchases"
    )
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    operation_price = models.DecimalField(max_digits=10, decimal_places=2)
    operation_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Purchase of {self.quantity} shares of {self.stock.ticker} at {self.operation_price} by {self.user_stock.user}"


class StockPrice(models.Model):
    stock = models.ForeignKey(
        "Stock",
        on_delete=models.CASCADE,
        related_name="historical_prices",
        help_text="The stock this price data belongs to",
    )
    date = models.DateField(help_text="The date for this price data")
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    highest_price = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ["date"]
        unique_together = ("stock", "date")
        verbose_name = "Stock Price"
        verbose_name_plural = "Stock Prices"

    def __str__(self):
        return f"{self.stock.ticker} = {self.date}: Close ${self.close_price}"
