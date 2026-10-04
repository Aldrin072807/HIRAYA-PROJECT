from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, InterviewSession, AnswerSubmission

def start_interview(request):
    """Creates a new interview session and redirects to the first question."""
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        if not user:
            return redirect('login')

        session = InterviewSession.objects.create(user=user)
        first_question = Question.objects.first()

        if first_question:
            return redirect('interviews:interview_question', session_id=session.id, question_id=first_question.id)

    return render(request, 'interviews/start.html')


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

    context = {
        'session': session,
        'question': question,
    }
    return render(request, 'interviews/question.html', context)


def interview_results(request, session_id):
    """Displays all answered questions and responses for a completed session."""
    session = get_object_or_404(InterviewSession, id=session_id)
    submissions = AnswerSubmission.objects.filter(session=session).select_related('question')

    context = {
        'session': session,
        'submissions': submissions,
    }
    return render(request, 'interviews/results.html', context)
    