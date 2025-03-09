import logging

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from wallets.models import Wallet


class HomeView(TemplateView):
    template_name = "payments/pay_home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            price_id = "price_1QiihBCTdBnXvy6wjmPUL417"
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=request.build_absolute_uri(reverse("payment-success")),
                cancel_url=request.build_absolute_uri(reverse("payment-failure")),
                metadata={"wallet_id": request.user.wallet.id},
            )
            request.session["checkout_session_id"] = checkout_session.id
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(request, self.template_name, {"error": str(e)})


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    if event.type == "checkout.session.completed":
        payment_succeeded = event.data.object
        user_id = payment_succeeded.get("metadata", {}).get("wallet_id")
        wallet = get_object_or_404(Wallet, pk=user_id)
        wallet_increase = payment_succeeded["amount_total"]
        wallet.balance += wallet_increase
        wallet.save()
    elif event.type == "charge.succeeded":
        logging.info("Event type: charge.succeeded")
    else:
        logging.info("Unhandled event type")

    return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = "payments/pay_success.html"


class FailureView(TemplateView):
    template_name = "payments/pay_failure.html"
