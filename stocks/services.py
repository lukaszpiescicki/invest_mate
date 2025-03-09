import logging
from decimal import Decimal

from django.db import transaction

from users.models import CustomUser

from .models import Stock, StockOperation, UserStock


@transaction.atomic
def buy_stock(user: CustomUser, stock: Stock, quantity: int) -> None:
    last_prices: dict = stock.get_last_prices
    if "close_price" in last_prices:
        price: Decimal = last_prices["close_price"]
        total_cost: Decimal = price * quantity

        if user.wallet.balance < total_cost:
            raise ValueError("You don't have enough money")

        user.wallet.balance -= total_cost
        user.wallet.save()
    else:
        logging.warning("No close price available")
    user_stock, created = UserStock.objects.get_or_create(
        user=user,
        stock=stock,
        defaults={"total_quantity": 0, "average_purchase_price": Decimal("0.00")},
    )
    total_cost: Decimal = (
        user_stock.average_purchase_price * user_stock.total_quantity
    ) + (price * quantity)
    user_stock.total_quantity += quantity
    user_stock.average_purchase_price = total_cost / user_stock.total_quantity
    user_stock.save()

    StockOperation.objects.create(
        user_stock=user_stock, stock=stock, quantity=quantity, operation_price=price
    )


@transaction.atomic
def sell_stock(user: CustomUser, stock: Stock, quantity: int) -> UserStock:
    user_stock: UserStock = UserStock.objects.filter(user=user, stock=stock).first()
    if not user_stock or user_stock.total_quantity < quantity:
        raise ValueError("Not enough stock to sell")
    last_prices = stock.get_last_prices
    if "close_price" in last_prices:
        price: Decimal = last_prices["close_price"]
        total_proceeds: Decimal = price * quantity

        user_stock.total_quantity -= quantity
        if user_stock.total_quantity == 0:
            user_stock.average_purchase_price = Decimal("0.00")
        user_stock.save()

        StockOperation.objects.create(
            user_stock=user_stock,
            stock=stock,
            quantity=quantity,
            operation_price=price,
        )

        user.wallet.balance += total_proceeds
        user.wallet.save()

    return user_stock
