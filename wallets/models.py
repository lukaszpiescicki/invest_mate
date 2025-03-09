from django.db import models


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stripe_payment_intent = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Wallet Balance: {self.balance}"
