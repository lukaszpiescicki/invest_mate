import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests
from django.conf import settings

from .models import Stock, StockPrice


class PolygonAPI:
    BASE_URL: str = "https://api.polygon.io/v3/reference/tickers"

    def __init__(self, api_key: Optional[str] = None, limit: int = 1000) -> None:
        self.api_key = api_key or settings.POLYGON_API_KEY
        if self.api_key is None:
            raise ValueError("API key must be provided")
        self.limit = limit

    def fetch_tickers(self, stock_ticker: str) -> None:
        """
        Fetch stock data from Polygon and Create Stock object with data from Polygon
        :param stock_ticker: string representing the stock ticker
        :return: None
        """
        base_url: str = "https://api.polygon.io/v3/reference/tickers"
        url: str = f"{base_url}/{stock_ticker}"

        response = self.make_request(url)
        if "results" in response:
            data: dict[str, Any] = response["results"]
            keys: List[str] = [
                "name",
                "description",
                "homepage_url",
                "sic_description",
                "market_cap",
            ]
            for key in keys:
                if key not in data:
                    data[key] = None

            defaults: dict = {
                "name": data.get("name"),
                "description": data.get("description"),
                "homepage": data.get("homepage_url"),
                "sector": data.get("sic_description"),
                "market_cap": data.get("market_cap"),
                "address1": data.get("address", {}).get("address1"),
                "city": data.get("address", {}).get("city"),
            }

            Stock.objects.update_or_create(ticker=stock_ticker, defaults=defaults)

    def make_request(self, url: str) -> Dict[str, Any]:
        """
        Make request to Polygon API
        :param url: string representing url from which data will be requested.
        :return: JSON response while succeed or {} if failed.
        """
        try:
            response = requests.get(
                url, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from Polygon.io: {e}")
            return {}

    def _create_ticker_url(
        self,
        base_url: str,
        stock_ticker: str,
        multiplier: int,
        timespan: str,
        from_date: str,
        to_date: str,
    ) -> str:
        """
        Create url for make_request() method
        :param base_url: string representing url from which data will be requested.
        :param stock_ticker: string representing the stock ticker
        :param multiplier: int of the size of the timespan multiplier.
        F.e. if timespan = 'minute' and multiplier = 5, then 5-minute bars will be returned
        :param timespan: The size of the time window ('minute', 'day', ...).
        :param from_date: The start of the aggregate time window
        :param to_date: The end of the aggregate time window.
        :return: String representing url for make_request()
        """
        url: str = f"{base_url}{stock_ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}?adjusted=true&sort=asc"

        return url

    def fetch_ticker_data(
        self,
        stock_ticker: str,
        multiplier: int,
        timespan: str,
        from_date: str,
        to_date: str,
    ) -> None:
        """
        Fetches price data for a given stock
        :param stock_ticker: string representing the stock ticker
        :param multiplier: int of the size of the timespan multiplier.
        F.e. if timespan = 'minute' and multiplier = 5, then 5-minute bars will be returned
        :param timespan: The size of the time window ('minute', 'day', ...).
        :param from_date: The start of the aggregate time window
        :param to_date: The end of the aggregate time window.
        :return: Create or update Stock object with price data for the given stock ticker.
        """
        base_url: str = "https://api.polygon.io/v2/aggs/ticker/"

        url: str = self._create_ticker_url(
            base_url, stock_ticker, multiplier, timespan, from_date, to_date
        )
        response: Dict[str, Any] = self.make_request(url)
        if "results" in response:
            data: List[Dict[str, Any]] = response["results"]
            for ticker_data in data:
                Stock.objects.update_or_create(
                    ticker=stock_ticker,
                    defaults={
                        "close_price": ticker_data.get("c"),
                        "highest_price": ticker_data.get("h"),
                        "lowest_price": ticker_data.get("l"),
                        "open_price": ticker_data.get("o"),
                        "volume": ticker_data.get("v"),
                    },
                )
        else:
            logging.warning("No data")

    def fetch_and_store_historical_prices(
        self,
        stock_ticker: str,
        multiplier: int,
        timespan: str,
        from_date: str,
        to_date: str,
    ) -> None:
        """
        Fetches stock prices and stores in database using requests.
        :param stock_ticker: string representing the stock ticker
        :param multiplier: int of the size of the timespan multiplier.
        F.e. if timespan = 'minute' and multiplier = 5, then 5-minute bars will be returned
        :param timespan: The size of the time window ('minute', 'day', ...).
        :param from_date: The start of the aggregate time window
        :param to_date:  The end of the aggregate time window.
        :return: Create or update StockPrice object with price data for the given stock ticker.
        """
        base_url: str = "https://api.polygon.io/v2/aggs/ticker/"

        url: str = self._create_ticker_url(
            base_url, stock_ticker, multiplier, timespan, from_date, to_date
        )
        response: Dict[str, Any] = self.make_request(url)
        if "results" in response:
            data: List[Dict[str, Any]] = response["results"]
            stock = Stock.objects.filter(ticker=stock_ticker).first()
            for price_data in data:
                date = datetime.fromtimestamp(
                    price_data["t"] / 1000, timezone.utc
                ).date()
                StockPrice.objects.update_or_create(
                    stock=stock,
                    date=date,
                    defaults={
                        "close_price": price_data.get("c"),
                        "highest_price": price_data.get("h"),
                        "lowest_price": price_data.get("l"),
                        "open_price": price_data.get("o"),
                        "volume": price_data.get("v"),
                    },
                )
            logging.info(f"Historical prices for {stock_ticker} have been updated.")
        else:
            logging.warning("No data")
