from django.shortcuts import render, redirect
from .models import Student

def student_login(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(name=name, password=password)
            # store student ID in session
            request.session['student_id'] = student.id
            return redirect("student_dashboard")
        except Student.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid name or password"})

    return render(request, "login.html")


def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect("student_login")  # not logged in

    student = Student.objects.get(id=student_id)
    return render(request, "dashboard.html", {"student": student})


def student_logout(request):
    try:
        del request.session['student_id']
    except KeyError:
        pass
    return redirect("student_login")


def mcq_test(request):
    if 'student_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        selected_questions_ids = request.session.get('selected_questions')
        if not selected_questions_ids:
            return redirect('mcq_test')

        selected_questions = Question.objects.filter(id__in=selected_questions_ids)

        score = 0
        answers_review = []  # store each question, selected, correct

        for question in selected_questions:
            selected_option = request.POST.get(f'question_{question.id}')
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

        # Save to student
        student_id = request.session.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        student.score = score
        student.total_questions = len(selected_questions)
        student.save()

        # Save results in session (for review page)
        request.session['score'] = score
        request.session['total_questions'] = len(selected_questions)
        request.session['answers_review'] = answers_review  

        return redirect('review')  # go to review page ✅

    else:
        questions = list(Question.objects.all())
        random.shuffle(questions)
        selected_questions = questions[:30]  # pick first 30
        selected_questions_ids = [q.id for q in selected_questions]
        request.session['selected_questions'] = selected_questions_ids

    context = {
        'questions': selected_questions,
    }
    return render(request, 'main/mcq_test.html', context)

    if 'student_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        selected_questions_ids = request.session.get('selected_questions')
        if not selected_questions_ids:
            return redirect('mcq_test')

        selected_questions = Question.objects.filter(id__in=selected_questions_ids)

        score = 0
        answers_review = []  # store each question, selected, correct

        for question in selected_questions:
            selected_option = request.POST.get(f'question_{question.id}')
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

        # Save to student
        student_id = request.session.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        student.score = score
        student.total_questions = len(selected_questions)
        student.save()

        # Save results in session
        request.session['score'] = score
        request.session['total_questions'] = len(selected_questions)
        request.session['answers_review'] = answers_review  # <-- new

        return redirect('review')  # go to new review page

    else:
        questions = list(Question.objects.all())
        random.shuffle(questions)
        selected_questions = questions[:30]
        selected_questions_ids = [q.id for q in selected_questions]
        request.session['selected_questions'] = selected_questions_ids

    context = {
        'questions': selected_questions,
    }
    return render(request, 'main/mcq_test.html', context)

from django.shortcuts import render, redirect
from .models import Question

def review(request):
    answers = request.session.get("answers", [])
    score = request.session.get("score", 0)
    total = request.session.get("total", 0)

    return render(request, "review.html", {
        "answers": answers,
        "score": score,
        "total": total
    })

def testpanel(request):
    return render(request, 'test.html')