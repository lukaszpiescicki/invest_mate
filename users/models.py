# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from wallets.models import Wallet
from workbooks.models import Workbook


class CustomUser(AbstractUser):
    email = models.EmailField()
    workbook = models.ForeignKey(Workbook, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.workbook:
            workbook = Workbook.objects.create(name=f"{self.first_name}'s Workbook")
            self.workbook = workbook
        if not self.wallet:
            wallet = Wallet.objects.create(balance=0.00)
            self.wallet = wallet

        super().save(*args, **kwargs)
