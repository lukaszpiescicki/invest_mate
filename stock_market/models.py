from django.db import models


class StockMarket(models.Model):
    name = models.CharField(max_length=20)
