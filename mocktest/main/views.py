from .models import  Student, Subject,Question, TestResult
import random
from django.shortcuts import render, redirect, get_object_or_404
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


from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from .models import Student, Subject, Question, TestResult


def mcq_test(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student = get_object_or_404(Student, student_id=request.session['student_id'])
    subjects = Subject.objects.all()
    selected_subject = request.GET.get('subject')

    if request.method == 'POST':
        score = 0
        total = 0
        answers_review = []
        selected_subject_obj = None

        for key, value in request.POST.items():
            if key.startswith("question_"):
                qid = key.split("_")[1]
                try:
                    question = Question.objects.get(id=qid)
                    selected_subject_obj = question.subject
                    total += 1
                    correct = (value == question.correct_answer)
                    if correct:
                        score += 1

                    # ✅ Always add each answered question to review
                    answers_review.append({
                        "question": question.question_text,        # ✅ fixed field name
                        "selected": value,
                        "correct": question.correct_answer,
                        "is_correct": correct,
                    })

                except Question.DoesNotExist:
                    continue

        # ✅ Save test result if we found a subject
        if selected_subject_obj:
            TestResult.objects.create(
                student=student,
                subject=selected_subject_obj,
                score=score,
                total_questions=total,
                attempt_no=TestResult.objects.filter(student=student, subject=selected_subject_obj).count() + 1
            )

        # ✅ Always set session values
        request.session['score'] = score
        request.session['total_questions'] = total
        request.session['answers_review'] = answers_review
        request.session['selected_subject'] = selected_subject
        request.session.modified = True

        return redirect("result")

    # ✅ GET: Show random 30 questions
    questions = []
    if selected_subject:
        questions = Question.objects.filter(subject__name=selected_subject).order_by("?")[:30]

    return render(request, 'test.html', {
        'subjects': subjects,
        'questions': questions,
        'selected_subject': selected_subject,
    })



def submit_test(request):
    """Optional if you want a separate submit URL — 
       but mcq_test already handles POST correctly."""
    if request.method == "POST":
        return mcq_test(request)   # reuse same logic
    return redirect("dashboard")


from django.shortcuts import render, redirect
from datetime import date
from .models import Student

def result(request):
    if 'student_id' not in request.session:
        return redirect('login')
    studentid = request.session['student_id']
    student = Student.objects.filter(student_id=studentid).first()
    if not student:
        return render(request, "result.html", {"error": f"No student found with ID {studentid}"})

    score = int(request.session.get('score', 0))
    print("Score from session:", score)  # Debugging line
    total = int(request.session.get('total_questions', 0))
    answers_review = request.session.get('answers_review', [])
    selected_subject = request.session.get('selected_subject', "N/A")
    percentage = (score / 30 * 100) if total > 0 else 0
    context = {
        'student_id': student.student_id,
        'firstname': student.firstname,
        'lastname': student.lastname,
        'score': score,
        'total': total,
        'percentage': round(percentage, 2),
        'answers_review': answers_review,
        'test_date': date.today().strftime("%d-%m-%Y"),
        'subject': selected_subject,
    }
    return render(request, 'result.html', context)



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





