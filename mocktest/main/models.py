from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # You might want to hash this password in practice
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_date = models.DateTimeField(default=timezone.now)
    batch_name = models.CharField(max_length=100, default='')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)

    def __str__(self):
        return self.name
