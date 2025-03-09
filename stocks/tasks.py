import time
from datetime import date, timedelta

from celery import shared_task
from django.conf import settings

from stocks.management.commands import consts

from .polygon_api import PolygonAPI


@shared_task
def fetch_tickers_task() -> None:
    api = PolygonAPI(settings.POLYGON_API_KEY)
    tickers = consts.tickers
    for ticker in tickers:
        time.sleep(11)
        api.fetch_tickers(ticker)


@shared_task
def fetch_ticker_data_task() -> None:
    tickers = consts.tickers
    multiplier = 1
    timespan = "day"
    from_date = str(date.today() - timedelta(days=2))
    to_date = str(date.today())
    api = PolygonAPI(settings.POLYGON_API_KEY)
    for ticker in tickers:
        time.sleep(11)
        api.fetch_ticker_data(ticker, multiplier, timespan, from_date, to_date)


@shared_task
def fetch_and_store_historical_prices_task() -> None:
    tickers = consts.tickers
    multiplier = 1
    timespan = "day"
    from_date = str(date.today() - timedelta(days=2))
    to_date = str(date.today())
    api = PolygonAPI(settings.POLYGON_API_KEY)
    for ticker in tickers:
        time.sleep(11)
        api.fetch_and_store_historical_prices(
            ticker, multiplier, timespan, from_date, to_date
        )
