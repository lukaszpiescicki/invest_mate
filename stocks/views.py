from datetime import timedelta

import pandas as pd
import plotly.express as px
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import StockBuySellForm
from .models import Stock, StockPrice
from .services import buy_stock, sell_stock


class StockListView(ListView):
    model = Stock
    template_name = "stocks/stocks.html"
    context_object_name = "stocks"
    ordering = ["ticker"]


class StockDetailView(DetailView):
    model = Stock
    template_name = "stocks/stock.html"
    context_object_name = "stock"
    slug_field = "ticker"
    slug_url_kwarg = "ticker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        stock = self.get_object()
        form = StockBuySellForm()
        context.update(**stock.get_last_prices)

        seven_days_ago = now().date() - timedelta(days=7)
        prices = StockPrice.objects.filter(
            stock=stock, date__gte=seven_days_ago
        ).order_by("date")

        dates = [price.date for price in prices]
        close_prices = [price.close_price for price in prices]

        df = pd.DataFrame({"Date": dates, "Close Price": close_prices})
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        filtered_df = df[df["Date"] >= seven_days_ago]
        fig = px.line(
            filtered_df,
            x="Date",
            y="Close Price",
            labels={"x": "Date", "y": "Price"},
            markers=True,
        )
        fig.update_layout(xaxis=dict(type="category"))
        chart_html = fig.to_html(full_html=False)
        context["form"] = form
        context["chart"] = chart_html
        return context


class StockBuySellView(LoginRequiredMixin, View):
    model = Stock
    context_object_name = "stock"
    slug_field = "ticker"
    slug_url_kwarg = "ticker"

    def post(self, request, stock_id):
        stock = get_object_or_404(Stock, id=stock_id)
        form = StockBuySellForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            operation = request.POST.get("operation")

            if "buy" in operation:
                try:
                    buy_stock(request.user, stock, quantity)
                    messages.success(
                        self.request,
                        f"You successfully bought {quantity} shares of {stock.name}!",
                    )
                except ValueError:
                    messages.error(request, "Try again later")
            elif "sell" in operation:
                try:
                    sell_stock(request.user, stock, quantity)
                    messages.success(
                        self.request,
                        f"You successfully sold {quantity} shares of {stock.name}!",
                    )
                except ValueError:
                    messages.error(request, "Try again later")
            else:
                messages.error(request, "Invalid action")
        else:
            messages.error(request, "Invalid form submission.")

        return redirect(reverse("stock-detail", args=[stock.ticker]))
