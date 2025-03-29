from django.urls import path

from . import views

app_name = "paper_questions"
urlpatterns = [
    # Homepage
    path("", views.question, name="index"),
    path("solution", views.solution, name="solution"),
]
