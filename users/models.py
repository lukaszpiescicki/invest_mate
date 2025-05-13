# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from wallets.models import Wallet
from workbooks.models import Workbook


class CustomUser(AbstractUser):
    email = models.EmailField()
    workbook = models.OneToOneField(
        Workbook, on_delete=models.CASCADE, blank=True, null=True
    )
    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if self.workbook is None:
            workbook = Workbook.objects.create(name=f"{self.first_name}'s Workbook")
            self.workbook = workbook

        if self.wallet is None:
            wallet = Wallet.objects.create(balance=0.00)
            self.wallet = wallet

        return super(CustomUser, self).save(*args, **kwargs)
