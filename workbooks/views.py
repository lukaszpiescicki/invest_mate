from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .models import Answer, Category, Question, Quiz, Theory, Workbook


class WorkbookDetailView(DetailView):
    model = Workbook
    template_name = "workbook.html"
    context_object_name = "workbook"


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "quiz.html"
    context_object_name = "workbook"

    def get_object(self, queryset=None):
        workbook_id = self.kwargs.get("pk")
        quiz_id = self.kwargs.get("quiz_id")

        quiz = get_object_or_404(Quiz, id=quiz_id, workbook__id=workbook_id)

        return quiz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workbook"] = get_object_or_404(Workbook, id=self.kwargs.get("pk"))

        return context


class QuizCreateView(CreateView):
    permission_required = "quiz.add_quiz"
    model = Quiz
    template_name = "quiz_form.html"
    fields = ["title", "question", "answer", "category"]

    def form_valid(self, form):
        form.instance.author = self.request
        return super().form_valid(form)


class QuizUpdateView(UpdateView):
    permission_required = "quiz.change_quiz"
    model = Quiz
    template_name = "quiz_form.html"
    fields = ["title", "question", "answer", "category"]

    def test_func(self):
        quiz = self.get_object()
        return self.request.user == quiz.author


class QuestionCreateView(CreateView):
    permission_required = "question.add_question"
    model = Question
    template_name = "question_form.html"
    fields = ["text", "category"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    permission_required = "question.change_question"
    model = Question
    template_name = "question_form.html"
    fields = ["text", "category"]

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author


class QuestionDeleteView(DeleteView):
    permission_required = "question.delete_question"
    model = Question
    template_name = "delete_confirm.html"
    success_url = "/"

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author


class AnswerCreateView(CreateView):
    permission_required = "answer.add_answer"
    model = Answer
    template_name = "answer_form.html"
    fields = ["text", "question", "is_correct"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnswerUpdateView(UpdateView):
    permission_required = "answer.change_answer"
    model = Answer
    template_name = "answer_form.html"
    fields = ["text", "question", "is_correct"]

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author


class AnswerDeleteView(DeleteView):
    permission_required = "answer.delete_answer"
    model = Answer
    template_name = "delete_confirm.html"
    success_url = ""

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author


class TheoryCreateView(CreateView):
    permission_required = "theory.add_theory"
    model = Theory
    template_name = "theory_form.html"
    fields = ["text", "category"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TheoryUpdateView(UpdateView):
    permission_required = "theory.change_theory"
    model = Theory
    template_name = "theory_form.html"
    fields = ["text", "category"]

    def test_func(self):
        theory = self.get_object()
        return self.request.user == theory.author


class TheoryDeleteView(DeleteView):
    permission_required = "theory.delete_answer"
    model = Theory
    template_name = "delete_confirm.html"
    success_url = ""

    def test_func(self):
        theory = self.get_object()
        return self.request.user == theory.author


class CategoryCreateView(CreateView):
    permission_required = "category.add_category"
    model = Category
    template_name = "category_form.html"
    fields = ["text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    permission_required = "category.change_category"
    model = Category
    template_name = "category_form.html"
    fields = ["text"]

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.author


class CategoryDeleteView(DeleteView):
    permission_required = "category.delete_category"
    model = Category
    template_name = "delete_confirm.html"
    success_url = ""

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.author
