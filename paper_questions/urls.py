from django.urls import path

import paper_questions.views as views

app_name = "paper_questions"
urlpatterns = [
    path("", views.home, name="home"),
    path("questions/<str:subjects>", views.question, name="question.random"),
    path(
        "questions/<str:subjects>/<str:subject>/<int:question>",
        views.question,
        name="question",
    ),
    path(
        "solutions/<str:subjects>/<str:subject>/<int:question>",
        views.solution,
        name="solution",
    ),
    path("attempt/<str:subjects>", views.attempt, name="attempt"),
    path("custom_study", views.custom_study, name="custom_study.start"),
]
