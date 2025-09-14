from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import OuterRef, Subquery, IntegerField

from pgrind.models.problem import Problem
from pgrind.models.attempt import Attempt
from pgrind.models.subject import Subject
from django.db.models.functions import Coalesce


def home(request: HttpRequest):
    """Home"""
    # Subquery to get the most recent confidence per problem, defaulting to 0 if no record is found
    latest_confidence_subquery = (
        Attempt.objects.filter(problem=OuterRef("pk"))
        .order_by("-attempted_at")
        .values("confidence")[:1]
    )

    # Return 0 if no record is found
    latest_confidence_subquery = Coalesce(
        Subquery(latest_confidence_subquery, output_field=IntegerField()), 0
    )

    # Annotate each problem with its most recent confidence and group by subject
    subjects = [s for s in Subject.objects.distinct()]

    problems_by_subject = {
        subject: Problem.objects.filter(subject=subject)
        .annotate(most_recent_confidence=latest_confidence_subquery)
        .values("id", "most_recent_confidence")
        .order_by("id")
        for subject in subjects
    }

    return render(
        request,
        "pgrind/index.html",
        {
            "problems_by_subject": problems_by_subject,
        },
    )
