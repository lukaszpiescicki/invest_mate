from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..models import Category, Question, Quiz


class QuizListView(ListView):
    model = Quiz
    template_name = "workbooks/quiz.html"
    context_object_name = "quizzes"
    ordering = ["-author"]


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "workbooks/quiz_content.html"
    context_object_name = "quiz"


class QuizCreateView(CreateView):
    permission_required = "quiz.add_quiz"
    model = Quiz
    template_name = "workbooks/quiz_form.html"
    fields = ["title", "question", "category"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.workbook = self.request.user.workbook
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.all()
        context["categories"] = Category.objects.all()

        return context


class QuizUpdateView(UpdateView):
    permission_required = "quiz.change_quiz"
    model = Quiz
    template_name = "workbooks/quiz_form.html"
    fields = ["title", "question", "category"]

    def test_func(self):
        quiz = self.get_object()
        return self.request.user == quiz.author


class QuizDeleteView(DeleteView):
    permission_required = "quiz.delete_question"
    model = Quiz
    template_name = "workbooks/delete_confirm.html"
    success_url = "/"

    def test_func(self):
        quiz = self.get_object()
        return self.request.user == quiz.author
