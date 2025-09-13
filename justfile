IMAGE_TAG := `git rev-parse --short HEAD` # Currently checked out commit hash

dev:
    DJANGO_SETTINGS_MODULE=zackads.settings.dev uv run ./manage.py runserver
    xdg-open http://localhost:8000/

test:
    DJANGO_SETTINGS_MODULE=zackads.settings.dev uv run pytest

watch:
    DJANGO_SETTINGS_MODULE=zackads.settings.dev uv run ptw .

build:
    docker build -t zackads:{{IMAGE_TAG}} .