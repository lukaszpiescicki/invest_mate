from django.views.generic.list import ListView

from ..models import Article


class HomeView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "articles"
