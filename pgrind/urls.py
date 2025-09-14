from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings

from pgrind.views.home import home
from pgrind.views.question import question
from pgrind.views.solution import solution
from pgrind.views.upload import upload
from pgrind.views.error import error

app_name = "pgrind"
urlpatterns: list[URLPattern] = [
    path("", home, name="home"),
    path("upload", upload, name="upload"),
    path(
        "question/<int:id>",
        question,
        name="question",
    ),
    path("solution/<int:id>", solution, name="solution"),
    path("error", error, name="error"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
