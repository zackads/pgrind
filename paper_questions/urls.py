from django.urls import path

from . import views

app_name = "paper_questions"
urlpatterns = [
    path("", views.home, name="home"),
    path("question", views.question, name="question"),
    path("solution", views.solution, name="solution"),
    path("attempt", views.attempt, name="attempt"),
]
