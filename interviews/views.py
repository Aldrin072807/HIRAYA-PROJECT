from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import Question, InterviewSession, AnswerSubmission


def get_dashboard_url(user):
    """Returns the appropriate dashboard route based on user privileges."""
    if user.is_authenticated and user.is_staff:
        return 'profiles:admin_dashboard'
    return 'profiles:student_dashboard'


def get_default_questions():
    """Returns 5 fundamental computer industry interview questions."""
    industry_questions = [
        ("Technical", "What is the difference between a primary key and a foreign key in a relational database?"),
        ("Technical", "Explain how Object-Relational Mapping (ORM) works in web frameworks."),
        ("Technical", "Describe the difference between process and thread in operating systems."),
        ("Technical", "What are the core principles of Object-Oriented Programming (OOP)?"),
        ("Behavioral", "Describe a technical obstacle you faced during a project and how you resolved it.")
    ]
    
    questions = []
    for category, text in industry_questions:
        obj, _ = Question.objects.get_or_create(category=category, text=text)
        questions.append(obj)
    return questions


@login_required
def start_interview(request):
    """Creates an interview session and loads standard practice questions."""
    job_id = request.GET.get('job_id') or request.POST.get('job_id')
    job = get_object_or_404(Job, id=job_id) if job_id else None

    if request.method == 'POST':
        session = InterviewSession.objects.create(user=request.user, job=job)

        # Load standard industry questions
        questions = get_default_questions()
        first_question = questions[0] if questions else Question.objects.first()

        if first_question:
            return redirect('interviews:interview_question', session_id=session.id, question_id=first_question.id)

    dashboard_url = get_dashboard_url(request.user)
    context = {
        'job': job,
        'dashboard_url': dashboard_url,
    }
    return render(request, 'interviews/start.html', context)


@login_required
def interview_question(request, session_id, question_id):
    """Renders the current question and handles answer submissions."""
    session = get_object_or_404(InterviewSession, id=session_id)
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        user_answer = request.POST.get('answer', '')

        AnswerSubmission.objects.create(
            session=session,
            question=question,
            user_answer=user_answer
        )

        next_question = Question.objects.filter(id__gt=question.id).first()
        if next_question:
            return redirect('interviews:interview_question', session_id=session.id, question_id=next_question.id)
        else:
            session.completed = True
            session.save()
            return redirect('interviews:interview_results', session_id=session.id)

    dashboard_url = get_dashboard_url(request.user)
    context = {
        'session': session,
        'question': question,
        'dashboard_url': dashboard_url,
    }
    return render(request, 'interviews/question.html', context)


@login_required
def interview_results(request, session_id):
    """Displays all answered questions and responses for a completed session."""
    session = get_object_or_404(InterviewSession, id=session_id)
    submissions = AnswerSubmission.objects.filter(session=session).select_related('question')

    dashboard_url = get_dashboard_url(request.user)
    context = {
        'session': session,
        'submissions': submissions,
        'dashboard_url': dashboard_url,
    }
    return render(request, 'interviews/results.html', context)