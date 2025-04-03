from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..models import Category


class CategoryDetailView(DetailView):
    model = Category
    template_name = "workbooks/category_content.html"


class CategoryListView(ListView):
    model = Category
    template_name = "workbooks/category.html"
    context_object_name = "categories"
    ordering = ["-author"]
    paginate_by = 4


class CategoryCreateView(CreateView):
    permission_required = "category.add_category"
    model = Category
    template_name = "workbooks/category_form.html"
    fields = ["text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    permission_required = "category.change_category"
    model = Category
    template_name = "workbooks/category_form.html"
    fields = ["text"]

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.author


class CategoryDeleteView(DeleteView):
    permission_required = "category.delete_category"
    model = Category
    template_name = "workbooks/delete_confirm.html"
    success_url = ""

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.author
