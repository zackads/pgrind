from datetime import datetime, timezone

from django.db import models

from .static_file_problem import StaticFileProblem


class StaticFileProblemAttempt(models.Model):
    """
    Record the outcome of an attempt to answer a problem posed by the app, and thus determine when the question is next
    posed to the user.
    """

    class Confidence(models.IntegerChoices):
        NOT_ATTEMPTED = 0
        HARD = 1
        MEDIUM = 2
        EASY = 3

    problem = models.ForeignKey(StaticFileProblem, on_delete=models.CASCADE)
    attempted_at = models.DateTimeField(auto_now_add=True)
    confidence = models.IntegerField(choices=Confidence.choices)

    def __str__(self):
        return f"{self.problem} at {self.attempted_at}, confidence {self.confidence}"

    def days_ago(self, now: datetime = datetime.now(timezone.utc)) -> int:
        return (now - self.attempted_at).days
