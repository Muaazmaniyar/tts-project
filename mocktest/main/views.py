from .models import  Student, Subject,Question, TestResult
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from datetime import date
from django.shortcuts import render, redirect
from .models import Student

def student_login(request):
    if request.method == "POST":
        student_id = request.POST.get("name")
        password = request.POST.get("password")

        try:
            # check if student exists
            student = Student.objects.get(student_id=student_id, password=password)
            # store student ID (primary key) in session
            request.session['student_id'] = student.student_id   # ✅ store MCS001
            return redirect("dashboard")  # ✅ use url name, not template
        except Student.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid name or password"})

    return render(request, "login.html")


def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect("login")

    student = get_object_or_404(Student, student_id=student_id)
    return render(request, "dashboard.html", {"student": student})



def student_logout(request):
    try:
        del request.session['student_id']
    except KeyError:
        pass
    return redirect("login")



def start_test(request):
    subjects = Subject.objects.all()  # Get all available subjects

    if request.method == "POST":
        selected_subject_id = request.POST.get("subject")
        if selected_subject_id:
            subject = Subject.objects.get(id=selected_subject_id)
            return redirect(f'/test/?subject={subject.name}')
    
    return render(request, 'start_test.html', {'subjects': subjects})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject, Question

def mcq_test(request):
    subjects = Subject.objects.all()
    selected_subject = request.GET.get('subject')

    if request.method == 'POST':
        # ✅ Handle submitted answers
        submitted_answers = {}
        score = 0
        total = 0

        for key, value in request.POST.items():
            if key.startswith("question_"):
                qid = key.split("_")[1]
                try:
                    question = Question.objects.get(id=qid)
                    submitted_answers[qid] = value
                    total += 1
                    if value == question.correct_answer:
                        score += 1
                except Question.DoesNotExist:
                    continue

        # ✅ Clear any old answers (fresh test next time)
        if 'student_answers' in request.session:
            del request.session['student_answers']

        return render(request, 'result.html', {
            'score': score,
            'total': total,
            'submitted_answers': submitted_answers,
        })

    # ✅ GET: Show exam with random 30 questions
    if selected_subject:
        questions = Question.objects.filter(subject__name=selected_subject).order_by("?")[:30]
    else:
        questions = []

    # ✅ Ensure no old answers remain
    request.session['student_answers'] = {}

    context = {
        'subjects': subjects,
        'questions': questions,
        'selected_subject': selected_subject
    }
    return render(request, 'test.html', context)



def submit_test(request):
    if request.method == "POST":
        student_id = request.session.get("student_id")
        student = Student.objects.get(student_id=student_id)

        # Save student answers and score
        answers = request.POST
        score = 0
        total = 0
        for key, value in answers.items():
            if key.startswith("question_"):
                qid = int(key.split("_")[1])
                question = Question.objects.get(id=qid)
                total += 1
                if question.answer == value:
                    score += 1

        # Save result
        TestResult.objects.create(
            student=student,
            score=score,
            total=total,
            date=date.today()
        )

        # Redirect to new test instead of result
        return redirect("start_test")



def result(request):
    if 'student_id' not in request.session:
        return redirect('login')

    studentid = request.session['student_id']
    student = Student.objects.filter(student_id=studentid).first()
    if not student:
        return render(request, "result.html", {"error": f"No student found with ID {studentid}"})

    score = request.session.get('score', 0)
    total = request.session.get('total_questions', 0)
    answers_review = request.session.get('answers_review', [])
    
    # Calculate percentage
    percentage = (score / total * 100) if total > 0 else 0

    return render(request, 'result.html', {
        'student_id': student.student_id,
        'firstname': student.firstname,
        'lastname': student.lastname,
        'score': score,
        'total': total,
        'total_questions': total,       # needed for template
        'percentage': round(percentage, 2),
        'answers_review': answers_review,
        'test_date': date.today().strftime("%d-%m-%Y"),  # today’s date
    })

def test_history(request):
    if 'student_id' not in request.session:
        return redirect('login')

    studentid = request.session['student_id']
    student = get_object_or_404(Student, student_id=studentid)

    results = TestResult.objects.filter(student=student).order_by('-date_taken')

    return render(request, "test_history.html", {"student": student, "results": results})


def review(request):
    answers = request.session.get("answers_review", [])  # ✅ fixed name
    score = request.session.get("score", 0)
    total = request.session.get("total_questions", 0)   # ✅ fixed name

    return render(request, "review.html", {
        "answers": answers,
        "score": score,
        "total": total
    })





