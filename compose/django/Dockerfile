# Define an alias for the specific Python version used in this file.
FROM docker.io/python:3.12.3-slim-bookworm as python


# Python build stage
FROM python as python-build-stage


# Install necessary apt packages.
RUN apt-get update && apt-get install --no-install-recommends -y \
  # Dependencies for building Python packages.
  build-essential \
  # Dependencies for psycopg (PostgreSQL adapter).
  libpq-dev


# Copy the requirements file to the image.
COPY ./requirements.txt /requirements.txt


# Create Python dependency and sub-dependency wheels for caching.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r requirements.txt


# Python 'run' stage
FROM python as python-run-stage

ARG APP_HOME=/app


# Set environment variables to ensure Python output is not buffered and not to write .pyc files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


# Set the working directory.
WORKDIR ${APP_HOME}


# Install required system dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg dependencies.
  libpq-dev \
  # Translations dependencies.
  gettext \
  # Clean up unused files to reduce image size.
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


# Copy Python dependency wheels from the build stage.
COPY --from=python-build-stage /usr/src/app/wheels /wheels/


# Use wheels to install Python dependencies.
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/


# Install git in the run stage
RUN apt-get update && apt-get install -y git


# Copy and set up the entrypoint script.
COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


# Copy and set up the start script.
COPY ./compose/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


# Copy and set up the start script for celery worker.
COPY ./compose/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


# Copy and set up the start script.
COPY ./compose/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat


# Copy and set up the start script.
COPY ./compose/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


# Copy the application code to the working directory.
COPY . ${APP_HOME}


# Set the entrypoint for the container.
ENTRYPOINT ["/entrypoint"]
