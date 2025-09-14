from django.db import models


class Problem(models.Model):
    subject = models.CharField(max_length=255)
    question_file = models.FileField(upload_to="pgrind/problems/questions/")
    solution_file = models.FileField(upload_to="pgrind/problems/solutions/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.subject } : {self.pk}"
