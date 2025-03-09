from django.conf import settings
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
