import os
import random

from django.shortcuts import render
from django.templatetags.static import static

from pgrind.settings import STATIC_ROOT

files = [f for f in os.listdir(str(STATIC_ROOT) + "/paper_questions")]


def question_count(subject: str) -> int:
    return len([f for f in files if f.split("-")[0] == subject]) // 2


def index(request):
    """Home"""
    return render(request, "paper_questions/index.html")


def question(request):
    subjects = ["data", "prob_ii", "comp_arch"]
    subject = request.GET.get("subject") or random.choice(subjects)
    id = request.GET.get("id") or random.randint(1, question_count(subject))

    print(subject, question_count(subject))

    return render(
        request,
        "paper_questions/question.html",
        {
            "subject": subject,
            "id": id,
            "image_url": static(f"paper_questions/{subject}-q-{id}.png"),
            "solution_url": f"/solution?subject={subject}&id={id}",
        },
    )


def solution(request):
    subject = request.GET.get("subject")
    id = request.GET.get("id") or random.randint(1, 5)

    return render(
        request,
        "paper_questions/solution.html",
        {
            "image_url": static(f"paper_questions/{subject}-s-{id}.png"),
            "question_url": f"/?subject={subject}&id={id}",
            "next_url": "/",
        },
    )
