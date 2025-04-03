from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ..models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 4


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "blog/article_content.html"


class ArticleCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "blog.add_article"
    model = Article
    template_name = "blog/article_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "blog.change_article"
    model = Article
    template_name = "blog/article_form.html"
    fields = ["title", "content"]


class ArticleDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = "blog.delete_article"
    model = Article
    template_name = "blog/delete_confirm.html"
    success_url = "/"
