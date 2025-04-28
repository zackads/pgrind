from django import forms
from django.shortcuts import render, redirect

from paper_questions.models import StaticFileProblemAttempt, Subject


class CustomStudyForm(forms.Form):
    subjects = forms.MultipleChoiceField(
        choices=[(s.value, s.value) for s in Subject],
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white checked:border-gray-800 checked:bg-gray-800 indeterminate:border-gray-800 indeterminate:bg-gray-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 forced-colors:appearance-auto"
            }
        ),
        required=True,
        error_messages={"required": "Please select at least one subject."},
    )
    difficulties = forms.MultipleChoiceField(
        choices=[(d[1], d[1]) for d in StaticFileProblemAttempt.CONFIDENCE_CHOICES],
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white checked:border-gray-800 checked:bg-gray-800 indeterminate:border-gray-800 indeterminate:bg-gray-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 forced-colors:appearance-auto"
            }
        ),
        required=True,
        error_messages={"required": "Please select at least one difficulty level."},
    )


from django.http import HttpRequest


def custom_study(request: HttpRequest):
    """Custom study session"""
    if request.method == "POST":
        form = CustomStudyForm(request.POST)
        if form.is_valid():
            subjects = form.cleaned_data["subjects"]
            difficulties = form.cleaned_data["difficulties"]
            return redirect(
                "paper_questions:question.random",
                subjects="-".join(subjects),
                difficulties="-".join(difficulties),
            )
    else:
        form = CustomStudyForm()

    return render(
        request,
        "paper_questions/custom_study.html",
        {"form": form},
    )
