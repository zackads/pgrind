from django import forms


class SingleProblemUploadForm(forms.Form):
    subject = forms.CharField(label="Subject", max_length=100)
    question_image = forms.ImageField()
    solution_image = forms.ImageField()
