from django.urls import path
from . import views

app_name = "paper_questions"
urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    path('question', views.question, name='question'),
    path('solution', views.solution, name='solution')
]