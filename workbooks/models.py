from django.conf import settings
from django.db import models
from django.urls import reverse


class Workbook(models.Model):
    name = models.CharField(max_length=50)
    progress = models.IntegerField(default=0)


class Category(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="quiz_category",
    )

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.text


class Question(models.Model):
    text = models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="question",
    )

    def get_absolute_url(self):
        return reverse("question-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=200)
    question = models.ManyToManyField(Question)
    is_correct = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="answer",
    )

    def get_absolute_url(self):
        return reverse("answer-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.text


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    workbook = models.ForeignKey(
        Workbook, on_delete=models.DO_NOTHING, related_name="quizzes"
    )
    question = models.ManyToManyField(Question)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="quizzes",
    )

    def get_absolute_url(self):
        return reverse("quiz-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.title


class Theory(models.Model):
    text = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    workbook = models.ForeignKey(Workbook, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="theory",
    )

    def get_absolute_url(self):
        return reverse("theory-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.text
