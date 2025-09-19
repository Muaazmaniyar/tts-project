from .models import  Student, Subject, TestResult,Question
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib import messages
from datetime import date



def student_login(request):
    if request.method == "POST":
        user_id = request.POST.get("username")   # login with user_id
        password = request.POST.get("password")

        try:
            student = Student.objects.get(user_id=user_id)

            if student.password == password:  # (You should hash later)
                # Save session
                request.session['student_id'] = student.student_id   
                request.session['user_id'] = student.user_id
                request.session['first_login'] = not student.has_changed_password  

                # If password not changed yet → redirect to change password page
                if not student.has_changed_password:
                    return redirect("change_password")

                return redirect("dashboard")  
            else:
                messages.error(request, "Invalid username or password")

        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Fetch logged-in student
        student_id = request.session.get("student_id")
        if not student_id:
            messages.error(request, "You must be logged in to change password.")
            return redirect("login")

        student = Student.objects.get(student_id=student_id)

        # Check old password
        if student.password != old_password:
            messages.error(request, "Old password is incorrect.")
            return redirect("change_password")

        # Check confirm match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")

        # Update password & set flag
        student.password = new_password
        student.has_changed_password = True
        student.save()

        messages.success(request, "Password changed successfully.")
        return redirect("login")

    return render(request, "change_password.html")


def student_logout(request):
    try:
        del request.session['student_id']
    except KeyError:
        pass
    return redirect("login")



def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect("login")

    student = get_object_or_404(Student, student_id=student_id)

    subjects = Subject.objects.all()
    selected_subject_id = request.GET.get('subject')
    selected_subject = None
    chart_data = []

    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id)
    elif subjects:
        selected_subject = subjects.first()  

    if selected_subject:
        results = TestResult.objects.filter(student=student, subject=selected_subject).order_by('date_taken')
        chart_data = [
            {"date": r.date_taken.strftime("%d-%m-%Y"), "score": r.score, "total": r.total_questions}
            for r in results
        ]

    context = {
        "student": student,
        "subjects": subjects,
        "selected_subject": selected_subject,
        "chart_data": chart_data,
        "active_page": "dashboard",
    }
    return render(request, "progress.html", context)

def student_progress(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student = get_object_or_404(Student, student_id=request.session['student_id'])
    subjects = Subject.objects.all()  

    selected_subject_id = request.GET.get('subject')
    selected_subject = None
    chart_data = []

    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id)
        results = TestResult.objects.filter(student=student, subject=selected_subject).order_by('date_taken')

        chart_data = [
            {
                "date": result.date_taken.strftime("%d-%m-%Y"),
                "score": result.score,
                "total": result.total_questions
            }
            for result in results
        ]

    context = {
        "student": student,
        "subjects": subjects,
        "selected_subject": selected_subject,
        "chart_data": chart_data,
        "active_page": "dashboard", 
    }
    return render(request, "progress.html", context)



def start_test(request):
    subjects = Subject.objects.all()

    if request.method == "POST":
        selected_subject_id = request.POST.get("subject")
        if selected_subject_id:
            subject = Subject.objects.get(id=selected_subject_id)

           
            for key in ["exam_start_time", "selected_questions", "score", "total_questions", "answers_review", "selected_subject"]:
                request.session.pop(key, None)

            return redirect(f'/test/?subject={subject.name}')
    
    return render(request, 'start_test.html', {'subjects': subjects, "active_page": "start_test"})



from django.utils import timezone

def mcq_test(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student = get_object_or_404(Student, student_id=request.session['student_id'])
    subjects = Subject.objects.all()
    selected_subject = request.GET.get('subject')

    exam_duration = 60 * 60 

    if 'exam_start_time' not in request.session:
        request.session['exam_start_time'] = timezone.now().isoformat()

    start_time = timezone.datetime.fromisoformat(request.session['exam_start_time'])
    elapsed = (timezone.now() - start_time).total_seconds()
    remaining_time = exam_duration - int(elapsed)
    if remaining_time <= 0:
        return redirect("result")

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

                    answers_review.append({
                        "question": question.question_text,
                        "selected": value,
                        "correct": question.correct_answer,
                        "is_correct": correct,
                    })

                except Question.DoesNotExist:
                    continue

        if selected_subject_obj:
            TestResult.objects.create(
                student=student,
                subject=selected_subject_obj,
                score=score,
                total_questions=total,
                attempt_no=TestResult.objects.filter(student=student, subject=selected_subject_obj).count() + 1
            )

        request.session['score'] = score
        request.session['total_questions'] = total
        request.session['answers_review'] = answers_review
        request.session['selected_subject'] = selected_subject

        request.session.pop('exam_start_time', None)
        request.session.pop('selected_questions', None)

        request.session.modified = True
        return redirect("result")

    
    questions = []
    if selected_subject:
        if 'selected_questions' not in request.session:
            
            selected_ids = list(
                Question.objects.filter(subject__name=selected_subject)
                .order_by("?")
                .values_list("id", flat=True)[:30]
            )
            request.session['selected_questions'] = selected_ids
            request.session.modified = True
        else:
            selected_ids = request.session['selected_questions']

        questions = Question.objects.filter(id__in=selected_ids)

    return render(request, 'test.html', {
        'subjects': subjects,
        'questions': questions,
        'selected_subject': selected_subject,
        'remaining_time': remaining_time,
    })




def submit_test(request):
    """Optional if you want a separate submit URL — 
       but mcq_test already handles POST correctly."""
    if request.method == "POST":
        return mcq_test(request)
    return redirect("dashboard")


def result(request):
    if 'student_id' not in request.session:
        return redirect('login')
    studentid = request.session['student_id']
    student = Student.objects.filter(student_id=studentid).first()
    if not student:
        return render(request, "result.html", {"error": f"No student found with ID {studentid}"})

    score = int(request.session.get('score', 0))
    print("Score from session:", score)  
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
        "active_page": "result",
    }
    return render(request, 'result.html', context)



def test_history(request):
    if 'student_id' not in request.session:
        return redirect('login')

    studentid = request.session['student_id']
    student = get_object_or_404(Student, student_id=studentid)

    results = TestResult.objects.filter(student=student).order_by('-date_taken')

    return render(request, "test_history.html", {"student": student, "results": results, "active_page": "history"})


def review(request):
    
    answers = request.session.get("answers_review", []) 
    score = request.session.get("score", 0)
    total = request.session.get("total_questions", 0)   
    return render(request, "review.html", {
        "answers": answers,
        "score": score,
        "total": total
    })
