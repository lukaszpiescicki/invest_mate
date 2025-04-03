from django.contrib import admin

from .models import Answer, Category, Question, Quiz, Theory, Workbook

admin.site.register(Workbook)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Theory)
admin.site.register(Category)


class QuizAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")


admin.site.register(Quiz, QuizAdmin)
