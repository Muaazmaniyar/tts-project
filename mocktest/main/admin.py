from django.contrib import admin
from .models import Student,Subject,Question

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "firstname", "lastname")
    search_fields = ("student_id", "firstname", "lastname")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question_text", "correct_answer")


admin.site.register(Subject)