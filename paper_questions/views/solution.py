from django.shortcuts import render
from django.templatetags.static import static


def solution(request, subject, question):
    return render(
        request,
        "paper_questions/solution.html",
        {
            "subject": subject,
            "question": question,
            "image_url": static(f"paper_questions/{subject}-s-{question}.png"),
        },
    )
