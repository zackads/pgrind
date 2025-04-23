from django.http import HttpRequest
from django.shortcuts import render
from django.templatetags.static import static

from paper_questions.models import Subject


def solution(
    request: HttpRequest,
    subject: Subject,
    question: int,
    subjects: str = "all",
    difficulties: str = "all",
):
    return render(
        request,
        "paper_questions/solution.html",
        {
            "subjects": subjects,
            "difficulties": difficulties,
            "subject": subject,
            "question": question,
            "image_url": static(f"paper_questions/{subject}-s-{question}.png"),
        },
    )
