from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from pgrind.views.home import home
from pgrind.views.question import question
from pgrind.views.solution import solution
from pgrind.views.attempt import attempt
from pgrind.views.custom_study import custom_study
from pgrind.views.upload import upload
from pgrind.views.error import error

app_name = "pgrind"
urlpatterns = [
    path("", home, name="home"),
    path(
        "questions/<str:subjects>/<str:difficulties>",
        question,
        name="question.random",
    ),
    path(
        "questions/<str:subjects>/<str:difficulties>/<str:subject>/<int:question>",
        question,
        name="question",
    ),
    path(
        "solutions/<str:subjects>/<str:difficulties>/<str:subject>/<int:question>",
        solution,
        name="solution",
    ),
    path("attempt/<str:subjects>/<str:difficulties>", attempt, name="attempt"),
    path("custom_study", custom_study, name="custom_study"),
    path("upload", upload, name="upload"),
    path("error", error, name="error"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
