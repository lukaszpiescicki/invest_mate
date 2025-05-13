from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from ..models import Answer, Category, Question, Quiz


class QuizListView(ListView):
    model = Quiz
    template_name = "workbooks/quiz.html"
    context_object_name = "quizzes"
    ordering = ["-author"]


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "workbooks/quiz_content.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.object.question.all()

        question_answers = {}

        for question in questions:
            question_answers[question.id] = Answer.objects.filter(question=question)

        context["question_answers"] = question_answers
        return context


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


class QuizSubmitView(LoginRequiredMixin, View):
    template_name = "workbooks/quiz_content.html"

    def get_quiz(self, pk):
        return get_object_or_404(Quiz, pk=pk)

    def post(self, request, pk):
        quiz = self.get_quiz(pk)

        questions = quiz.question.all()
        total_questions = questions.count()
        correct_answers = 0
        question_results = []

        for question in questions:
            selected_answer_id = request.POST.get(f"question-{question.id}")

            if selected_answer_id:
                selected_answer = get_object_or_404(Answer, id=selected_answer_id)
                correct_answer = Answer.objects.filter(
                    question=question, is_correct=True
                ).first()

                is_correct = selected_answer.is_correct
                if is_correct:
                    correct_answers += 1

                question_results.append(
                    {
                        "question_text": question.text,
                        "user_answer_text": selected_answer.text,
                        "correct_answer_text": correct_answer.text
                        if correct_answer
                        else "No correct answer defined",
                        "is_correct": is_correct,
                    }
                )

        score_percentage = (
            (correct_answers / total_questions * 100) if total_questions > 0 else 0
        )

        if request.user.workbook and score_percentage >= 70:
            workbook = request.user.workbook
            workbook.progress += 10
            workbook.progress = min(workbook.progress, 100)
            workbook.save()

            messages.success(
                request, "Great job! Your workbook progress has been updated."
            )

        question_answers = {}
        for question in questions:
            question_answers[question.id] = Answer.objects.filter(question=question)

        context = {
            "quiz": quiz,
            "question_answers": question_answers,
            "quiz_results": True,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "score_percentage": round(score_percentage, 1),
            "question_results": question_results,
        }

        return render(request, self.template_name, context)

    def get(self, request, pk):
        return redirect("quiz-detail", pk=pk)
