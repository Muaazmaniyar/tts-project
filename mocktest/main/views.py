from .models import Question, Student, TestResult,Subject
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Student, TestResult
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
    if 'student_id' not in request.session:
        return redirect("login")
    else:
        subjects = Subject.objects.all()
    return render(request, "start_test.html", {"subjects": subjects})


def mcq_test(request):
    if 'student_id' not in request.session:
        return redirect('login')

    selected_questions_ids = request.session.get('selected_questions')

    if request.method == 'POST':
        selected_questions = Question.objects.filter(id__in=selected_questions_ids)
        score = 0
        answers_review = []

        # Store submitted answers in session
        student_answers = request.session.get('student_answers', {})

        for question in selected_questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option:
                student_answers[str(question.id)] = selected_option  # store as string keys
            is_correct = selected_option == question.correct_answer
            if is_correct:
                score += 1

            answers_review.append({
                'id': question.id,
                'question_text': question.question_text,
                'options': [question.option1, question.option2, question.option3, question.option4],
                'selected_option': selected_option,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
            })

        request.session['student_answers'] = student_answers  # ✅ save current answers
        request.session['score'] = score
        request.session['total_questions'] = len(selected_questions)
        request.session['answers_review'] = answers_review  

        # Save TestResult in DB
        studentid = request.session.get('student_id')
        student = get_object_or_404(Student, student_id=studentid)
        attempt_no = TestResult.objects.filter(student=student).count() + 1

        TestResult.objects.create(
            student=student,
            score=score,
            total_questions=len(selected_questions),
            attempt_no=attempt_no
        )

        if 'selected_questions' in request.session:
            del request.session['selected_questions']
        if 'student_answers' in request.session:
            del request.session['student_answers']

        return redirect('result')

    else:
        # Generate new set of random questions if no session data exists
        if not selected_questions_ids:
            questions = list(Question.objects.all())
            random.shuffle(questions)
            selected_questions = questions[:30]  # Pick 30 random questions
            selected_questions_ids = [q.id for q in selected_questions]
            request.session['selected_questions'] = selected_questions_ids
        else:
            selected_questions = Question.objects.filter(id__in=selected_questions_ids)

    # Get previously selected answers (only if test not yet submitted)
    student_answers = request.session.get('student_answers', {})

    context = {
        'questions': selected_questions,
        'student_answers': student_answers
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





