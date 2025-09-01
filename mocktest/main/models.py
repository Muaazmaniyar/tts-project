from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)  # username
    roll_no = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # storing plain text (for demo only!)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

from django.db import models

class Question(models.Model):
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text[:50]

