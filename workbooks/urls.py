from django.urls import path

from .views.answers import (
    AnswerCreateView,
    AnswerDeleteView,
    AnswerDetailView,
    AnswerListView,
    AnswerUpdateView,
)
from .views.categories import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
)
from .views.questions import (
    QuestionCreateView,
    QuestionDeleteView,
    QuestionDetailView,
    QuestionListView,
    QuestionUpdateView,
)
from .views.quizzes import (
    QuizCreateView,
    QuizDeleteView,
    QuizDetailView,
    QuizListView,
    QuizUpdateView,
)
from .views.theories import (
    TheoryCreateView,
    TheoryDeleteView,
    TheoryDetailView,
    TheoryListView,
    TheoryUpdateView,
)
from .views.workbooks import WorkbookDetailView

urlpatterns = [
    path("workbooks/<int:pk>/", WorkbookDetailView.as_view(), name="workbook"),
    path("quiz/", QuizListView.as_view(), name="quiz-list"),
    path("quiz/<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),
    path("quiz/new/", QuizCreateView.as_view(), name="quiz-create"),
    path("quiz/<int:pk>/update/", QuizUpdateView.as_view(), name="quiz-update"),
    path("quiz/<int:pk>/delete/", QuizDeleteView.as_view(), name="quiz-delete"),
    path("question/", QuestionListView.as_view(), name="question-list"),
    path("question/<int:pk>/", QuestionDetailView.as_view(), name="question-detail"),
    path("question/new/", QuestionCreateView.as_view(), name="question-create"),
    path(
        "question/<int:pk>/update/",
        QuestionUpdateView.as_view(),
        name="question-update",
    ),
    path(
        "question/<int:pk>/delete/",
        QuestionDeleteView.as_view(),
        name="question-delete",
    ),
    path("answer/", AnswerListView.as_view(), name="answer-list"),
    path("answer/<int:pk>/", AnswerDetailView.as_view(), name="answer-detail"),
    path("answer/new/", AnswerCreateView.as_view(), name="answer-create"),
    path("answer/<int:pk>/update/", AnswerUpdateView.as_view(), name="answer-update"),
    path("answer/<int:pk>/delete/", AnswerDeleteView.as_view(), name="answer-delete"),
    path("theory/", TheoryListView.as_view(), name="theory-list"),
    path("theory/<int:pk>/", TheoryDetailView.as_view(), name="theory-detail"),
    path("theory/new/", TheoryCreateView.as_view(), name="theory-create"),
    path("theory/<int:pk>/update/", TheoryUpdateView.as_view(), name="theory-update"),
    path("theory/<int:pk>/delete/", TheoryDeleteView.as_view(), name="theory-delete"),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("category/new/", CategoryCreateView.as_view(), name="category-create"),
    path(
        "category/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
]
