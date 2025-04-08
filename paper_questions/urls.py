from django.urls import path

from . import views

app_name = "paper_questions"
urlpatterns = [
    path("", views.home, name="home"),
    path("questions", views.random_question, name="random_question"),
    path("questions/<str:subject>/<int:question>", views.question, name="question"),
    path("solutions/<str:subject>/<int:question>", views.solution, name="solution"),
    path("attempt", views.attempt, name="attempt"),
]
