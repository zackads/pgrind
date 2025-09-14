from django import forms

from pgrind.models.Problem import Problem


class SingleProblemUploadForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ["subject", "question_file", "solution_file"]

    def clean(self):
        cleaned = super().clean()
        q = cleaned.get("question_file")
        s = cleaned.get("solution_file")
        if not q or not s:
            raise forms.ValidationError(
                "Both question_file and solution_file are required."
            )
        return cleaned
