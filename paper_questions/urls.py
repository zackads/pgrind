from django.urls import path

import paper_questions.views as views

app_name = "paper_questions"
urlpatterns = [
    path("", views.home, name="home"),
    path("questions", views.question, name="question.random"),
    path("questions/<str:subject>/<int:question>", views.question, name="question"),
    path("solutions/<str:subject>/<int:question>", views.solution, name="solution"),
    path("attempt", views.attempt, name="attempt"),
    path("custom_study", views.custom_study, name="custom_study.start"),
    path(
        "custom_study/<str:subjects>/",
        views.custom_study,
        name="custom_study.random_question",
    ),
    path(
        "custom_study/<str:subjects>/<str:subject>/<int:question>",
        views.custom_study,
        name="custom_study.question",
    ),
]
