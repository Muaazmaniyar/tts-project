from django.contrib import admin
from .models import Student, Subject, Question, TestResult

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'firstname', 'lastname')
    search_fields = ('student_id', 'firstname', 'lastname')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question_text', 'correct_answer')
    search_fields = ('question_text',)
    list_filter = ('subject',)

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'total_questions', 'attempt_no', 'date_taken')
    search_fields = ('student__student_id', 'student__firstname', 'student__lastname', 'subject__name')
    list_filter = ('subject', 'attempt_no', 'date_taken')
