from django.db import models

from django.db import models

class Student(models.Model):
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)  
    student_id = models.CharField(max_length=20, unique=True, editable=False,null=True, blank=True)  
    password = models.CharField(max_length=128 ,null=True, blank=True)  # ⚠ better to hash this

    def save(self, *args, **kwargs):
        if not self.student_id:  
            last_student = Student.objects.order_by('-id').first()
            if last_student and last_student.student_id:
                last_number = int(last_student.student_id.replace("MCS", ""))
                new_number = last_number + 1
            else:
                new_number = 1
            self.student_id = f"MCS{new_number:03d}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} - {self.firstname} {self.lastname}"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text[:50]

