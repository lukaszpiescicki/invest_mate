from django.urls import path

from .views import QuizDetailView, WorkbookDetailView

urlpatterns = [
    path("workbooks/<int:pk>/", WorkbookDetailView.as_view(), name="workbook"),
    path(
        "workbooks/<int:pk>/quiz/<int:quiz_id>/", QuizDetailView.as_view(), name="quiz"
    ),
]
