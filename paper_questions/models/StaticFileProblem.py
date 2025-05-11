import os
from typing import NewType
from django.db import models
from django.core.validators import MinValueValidator

from paper_questions.models.Subject import Subject
from pgrind.settings.base import STATIC_ROOT

files = [f for f in os.listdir(str(STATIC_ROOT) + "/paper_questions")]

ProblemURL = NewType("ProblemURL", str)


class StaticFileProblem:
    subject = models.CharField(
        max_length=50, choices=[(s.value, s.value) for s in Subject]
    )
    question_number = models.IntegerField(validators=[MinValueValidator(0)])
    static_url: ProblemURL

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "question_number"], name="unique_problem"
            )
        ]

    @staticmethod
    def question_count(subject: str) -> int:
        return len([f for f in files if f.split("-")[0] == subject]) // 2
