from django.urls import path

import pgrind.views as views

app_name = "pgrind"
urlpatterns = [
    path("", views.home, name="home"),
    path(
        "questions/<str:subjects>/<str:difficulties>",
        views.question,
        name="question.random",
    ),
    path(
        "questions/<str:subjects>/<str:difficulties>/<str:subject>/<int:question>",
        views.question,
        name="question",
    ),
    path(
        "solutions/<str:subjects>/<str:difficulties>/<str:subject>/<int:question>",
        views.solution,
        name="solution",
    ),
    path("attempt/<str:subjects>/<str:difficulties>", views.attempt, name="attempt"),
    path("custom_study", views.custom_study, name="custom_study"),
    path("error", views.error, name="error"),
]
