from datetime import datetime, timezone

from django.db import models

from .problem import Problem


class Attempt(models.Model):
    """
    Record the outcome of an attempt to answer a problem posed by the app, and thus determine when the question is next
    posed to the user.
    """

    class Confidence(models.IntegerChoices):
        NOT_ATTEMPTED = 0
        HARD = 1
        MEDIUM = 2
        EASY = 3

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    attempted_at = models.DateTimeField(auto_now_add=True)
    confidence = models.IntegerField(choices=Confidence.choices)

    def __str__(self):
        return f"{self.problem} at {self.attempted_at}, confidence {self.confidence}"

    def days_ago(self, now: datetime = datetime.now(timezone.utc)) -> int:
        return (now - self.attempted_at).days

    def days_ago_text(self, now: datetime = datetime.now(timezone.utc)) -> str:
        if self.days_ago() == 0:
            return "today"
        elif self.days_ago() == 1:
            return "yesterday"
        else:
            return str(self.days_ago()) + " days ago"
