from django.urls import path

from .views import FailureView, HomeView, SuccessView, my_webhook_view

urlpatterns = [
    path("payments/home/", HomeView.as_view(), name="payment-home"),
    path("payments/success/", SuccessView.as_view(), name="payment-success"),
    path("payments/failure/", FailureView.as_view(), name="payment-failure"),
    path("webhook", my_webhook_view, name="webhook"),
]
