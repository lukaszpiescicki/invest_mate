from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..models import Theory


class TheoryDetailView(DetailView):
    model = Theory
    template_name = "workbooks/theory_content.html"


class TheoryListView(ListView):
    model = Theory
    template_name = "workbooks/theory.html"
    context_object_name = "theories"
    ordering = ["-category"]
    paginate_by = 4


class TheoryCreateView(CreateView):
    permission_required = "theory.add_theory"
    model = Theory
    template_name = "workbooks/theory_form.html"
    fields = ["text", "category"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TheoryUpdateView(UpdateView):
    permission_required = "theory.change_theory"
    model = Theory
    template_name = "workbooks/theory_form.html"
    fields = ["text", "category"]

    def test_func(self):
        theory = self.get_object()
        return self.request.user == theory.author


class TheoryDeleteView(DeleteView):
    permission_required = "theory.delete_answer"
    model = Theory
    template_name = "workbooks/delete_confirm.html"
    success_url = ""

    def test_func(self):
        theory = self.get_object()
        return self.request.user == theory.author
