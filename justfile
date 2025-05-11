LOCATION := "europe-west2"
PROJECT_NAME := "pgrind"
PROJECT_NUMBER := "598517095867"
IMAGE_NAME := PROJECT_NAME
IMAGE_TAG := `git rev-parse --short HEAD` # Currently checked out commit hash
REPOSITORY_NAME := PROJECT_NAME + "-deploy"
FULLY_QUALIFIED_IMAGE_NAME := LOCATION + "-docker.pkg.dev/" + PROJECT_NAME + "/" + REPOSITORY_NAME + "/" + IMAGE_NAME
CLOUD_RUN_SERVICE_NAME := "app"
GCP_STATIC_FILES_BUCKET_NAME := "pgrind_static_files"

dev:
    DJANGO_SETTINGS_MODULE=pgrind.settings.dev uv run ./manage.py runserver
    xdg-open http://localhost:8000/

test:
    DJANGO_SETTINGS_MODULE=pgrind.settings.dev uv run pytest

watch:
    DJANGO_SETTINGS_MODULE=pgrind.settings.dev uv run ptw .

build:
    docker build -t {{FULLY_QUALIFIED_IMAGE_NAME}}:{{IMAGE_TAG}} .

deploy:
    #!/usr/bin/env bash
    gcloud auth configure-docker {{LOCATION}}-docker.pkg.dev --quiet
    docker push {{FULLY_QUALIFIED_IMAGE_NAME}}:{{IMAGE_TAG}}
    gsutil -m rsync -r ./paper_questions gs://{{GCP_STATIC_FILES_BUCKET_NAME}}/paper_questions
    gcloud run deploy {{CLOUD_RUN_SERVICE_NAME}} \
      --image {{FULLY_QUALIFIED_IMAGE_NAME}}:{{IMAGE_TAG}} \
      --platform managed \
      --region {{LOCATION}} \
      --allow-unauthenticated \
      --project {{PROJECT_NAME}} \
      --port 8000 \
      --update-secrets DJANGO_SECRET_KEY=projects/{{PROJECT_NUMBER}}/secrets/DJANGO_SECRET_KEY:latest \
      --set-env-vars DJANGO_ALLOWED_HOSTS=app-598517095867.europe-west2.run.app \
      --set-env-vars DJANGO_CSRF_TRUSTED_ORIGINS=https://app-598517095867.europe-west2.run.app \
      --add-volume name=static_files,type=cloud-storage,bucket={{GCP_STATIC_FILES_BUCKET_NAME}} \
      --add-volume-mount volume=static_files,mount-path=$(pwd)/staticfiles/questions