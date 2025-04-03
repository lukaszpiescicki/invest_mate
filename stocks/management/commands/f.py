import time
from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand

from stocks.polygon_api import PolygonAPI

from .consts import tickers as const_tickers


class Command(BaseCommand):
    def handle(self, *args, **options):
        polygon_api = PolygonAPI(settings.POLYGON_API_KEY)
        tickers = const_tickers
        multiplier = 1
        timespan = "day"
        from_date = str(date.today() - timedelta(days=2))
        to_date = str(date.today())
        for ticker in tickers:
            time.sleep(13)
            print(ticker)
            polygon_api.fetch_and_store_historical_prices(
                stock_ticker=ticker,
                multiplier=multiplier,
                timespan=timespan,
                from_date=from_date,
                to_date=to_date,
            )
            # polygon_api.fetch_ticker_data(ticker, multiplier, timespan, from_date, to_date)
            # polygon_api.fetch_tickers(ticker)
