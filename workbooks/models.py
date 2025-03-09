from django.conf import settings
from django.db import models


class Category(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="music_notes",
    )

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


class Answer(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    is_correct = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="answer",
    )


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="quiz",
    )


class Theory(models.Model):
    text = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="theory",
    )


class Workbook(models.Model):
    quizzes = models.ManyToManyField(Quiz)
    progress = models.IntegerField(default=0)
