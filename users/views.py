from io import BytesIO

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, ListView, UpdateView, View
from xhtml2pdf import pisa

from stocks.models import UserStock

from .forms import UserRegisterForm, UserUpdateForm
from .tasks import send_email_task
from .utils.activate_account import account_activation_token


class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = "Activation link has been sent to your email id"
        message = render_to_string(
            "users/user_active_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = form.cleaned_data.get("email")
        send_email_task.delay(mail_subject, message, to_email)
        username = form.cleaned_data.get("username")
        messages.success(
            self.request,
            f"Dear {username}, you have successfully signed up! Confirm your email address to activate your account.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, form.errors)

        return super().form_invalid(form)


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    form_class = UserUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile's been updated!")
        return super().form_valid(form)


class UserPortfolioView(LoginRequiredMixin, ListView):
    model = UserStock
    template_name = "portfolio.html"
    context_object_name = "user_stocks"

    def get_queryset(self):
        return (
            UserStock.objects.filter(user=self.request.user)
            .annotate(
                current_value=ExpressionWrapper(
                    F("total_quantity") * F("stock__historical_prices__close_price"),
                    output_field=DecimalField(max_digits=20, decimal_places=2),
                )
            )
            .order_by("-id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_investments = (
            UserStock.objects.filter(user=self.request.user).aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F("total_quantity") * F("average_purchase_price"),
                        output_field=DecimalField(max_digits=20, decimal_places=2),
                    )
                )
            )["total"]
            or 0
        )
        total_current_value = (
            UserStock.objects.filter(user=self.request.user).aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F("total_quantity")
                        * F("stock__historical_prices__close_price"),
                        output_field=DecimalField(max_digits=20, decimal_places=2),
                    )
                )
            )["total"]
            or 0
        )
        context["total_investments"] = total_investments
        context["total_current_value"] = total_current_value
        wallet_balance = (
            self.request.user.wallet.balance if hasattr(self.request, "user") else 0
        )
        total_stocks = self.get_queryset().count()
        context.update(
            {
                "total_investments": total_investments,
                "wallet_balance": wallet_balance,
                "total_stocks": total_stocks,
                "total_current_value": total_current_value,
            }
        )
        return context

    def render_to_pdf(self, context):
        html_content = render_to_string("users/portfolio_pdf.html", context)

        buffer = BytesIO()

        pisa_status = pisa.CreatePDF(html_content, dest=buffer)

        if pisa_status.err:
            return None

        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        if request.GET.get("export") == "pdf":
            context = self.get_context_data()
            context["user"] = self.request.user
            pdf = self.render_to_pdf(context)

            if pdf:
                response = HttpResponse(pdf, content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="portfolio.pdf"'
                return response
            else:
                return HttpResponse("Error generating PDF", status=500)

        return super().get(request, *args, **kwargs)


class UserActivationView(View):
    template_name = "users/activation.html"

    def get(self, request, uidb64, token, *args, **kwargs):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse(
                "Thank you for your email confirmation. Now you can login your account."
            )
        else:
            return HttpResponse("Activation link is invalid!")
