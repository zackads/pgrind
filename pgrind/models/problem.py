from django.db import models

from pgrind.models.subject import Subject


class Problem(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_image = models.ImageField(upload_to="pgrind/problems/questions/")
    solution_image = models.ImageField(upload_to="pgrind/problems/solutions/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.subject } : {self.pk}"
