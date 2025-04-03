from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..models import Answer, Question


class AnswerDetailView(DetailView):
    model = Answer
    template_name = "workbooks/answer_content.html"


class AnswerListView(ListView):
    model = Answer
    template_name = "workbooks/answer.html"
    context_object_name = "answers"
    ordering = ["-author"]
    paginate_by = 4


class AnswerCreateView(CreateView):
    permission_required = "answer.add_answer"
    model = Answer
    template_name = "workbooks/answer_form.html"
    fields = ["text", "question", "is_correct"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.all()

        return context


class AnswerUpdateView(UpdateView):
    permission_required = "answer.change_answer"
    model = Answer
    template_name = "workbooks/answer_form.html"
    fields = ["text", "question", "is_correct"]

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author


class AnswerDeleteView(DeleteView):
    permission_required = "answer.delete_answer"
    model = Answer
    template_name = "workbooks/delete_confirm.html"
    success_url = ""

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author
