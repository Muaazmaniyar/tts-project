from django.contrib import admin
from .models import Student, Subject, Question, TestResult

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id',)
    search_fields = ('student_id', 'password', 'firstname', 'lastname', 'user_id',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question_text', 'correct_answer')
    search_fields = ('question_text',)
    list_filter = ('subject',)
