import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import Question, InterviewSession, AnswerSubmission

def generate_ai_questions(job_title=None, job_description=None):
    """
    Generates practice questions based on job details using an LLM.
    Falls back to default practice questions if API/key is not configured.
    """
    try:
        import openai
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            raise ValueError("No API Key")

        client = openai.OpenAI(api_key=api_key)
        prompt = f"""
        Generate 3 technical/behavioral interview questions for the following position:
        Position: {job_title or 'General Software Developer'}
        Description: {job_description or 'General software development concepts'}

        Return ONLY a JSON array of objects with 'category' and 'text'. Example:
        [
            {{"category": "Technical", "text": "Explain primary vs foreign keys."}},
            {{"category": "Behavioral", "text": "Describe a challenging project."}}
        ]
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        data = json.loads(response.choices[0].message.content.strip())
        
        questions = []
        for q in data:
            obj, _ = Question.objects.get_or_create(
                category=q.get('category', 'General'),
                text=q.get('text', '')
            )
            questions.append(obj)
        return questions
    except Exception:
        # Fallback question generation if database is empty or API is offline
        fallback_data = [
            ("Technical", "What is the difference between a primary key and a foreign key?"),
            ("Technical", "Explain how Object-Relational Mapping (ORM) works in web frameworks."),
            ("Behavioral", "Describe a technical obstacle you faced during a project and how you resolved it.")
        ]
        questions = []
        for category, text in fallback_data:
            obj, _ = Question.objects.get_or_create(category=category, text=text)
            questions.append(obj)
        return questions


@login_required
def start_interview(request):
    """Creates an interview session and loads or generates practice questions."""
    job_id = request.GET.get('job_id') or request.POST.get('job_id')
    job = get_object_or_404(Job, id=job_id) if job_id else None

    if request.method == 'POST':
        session = InterviewSession.objects.create(user=request.user, job=job)

        # Generate or load questions
        questions = generate_ai_questions(
            job.title if job else None, 
            job.description if job else None
        )

        first_question = questions[0] if questions else Question.objects.first()

        if first_question:
            return redirect('interviews:interview_question', session_id=session.id, question_id=first_question.id)

    context = {'job': job}
    return render(request, 'interviews/start.html', context)


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