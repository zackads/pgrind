import random

from django.shortcuts import render
from django.templatetags.static import static

def index(request):
    """Home"""
    return render(request, 'paper_questions/index.html')

def question(request):
    subject = request.GET.get('subject') or 'comp_arch'
    id = request.GET.get('id') or random.randint(1, 5)

    return render(
        request,
        'paper_questions/question.html',
        {
            'subject': subject,
            'id': id,
            'image_url': static(f"paper_questions/{subject}-q-{id}.png"),
            'solution_url': f'/solution?subject={subject}&id={id}'
        })

def solution(request):
    subject = request.GET.get('subject')
    id = request.GET.get('id') or random.randint(1, 5)

    return render(
        request,
        'paper_questions/solution.html',
        {
            'subject': subject,
            'id': id,
            'image_url': static(f"paper_questions/{subject}-s-{id}.png"),
            'question_url': f'/question?subject={subject}&id={id}',
            'same_subject_question_url': f'/question?subject={subject}',
            'random_subject_question_url': f'/question',
        }
    )