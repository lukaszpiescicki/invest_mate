from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..models import Category, Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = "workbooks/question_content.html"


class QuestionListView(ListView):
    model = Question
    template_name = "workbooks/question.html"
    context_object_name = "questions"
    ordering = ["-category"]
    paginate_by = 4


class QuestionCreateView(CreateView):
    permission_required = "question.add_question"
    model = Question
    template_name = "workbooks/question_form.html"
    fields = ["text", "category"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        return context


class QuestionUpdateView(UpdateView):
    permission_required = "question.change_question"
    model = Question
    template_name = "workbooks/question_form.html"
    fields = ["text", "category"]

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author


class QuestionDeleteView(DeleteView):
    permission_required = "question.delete_question"
    model = Question
    template_name = "workbooks/delete_confirm.html"
    success_url = "/"

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author
