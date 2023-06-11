FROM --platform=linux/amd64 python:3.10.10-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG PYPI_TOKEN
ENV PYPI_TOKEN $PYPI_TOKEN

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Install git to get local libs from gitlab
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# librdkafka build, this is needed for macOS wheel build.
RUN apt-get -y install libssl-dev # libsasl2-dev libsasl2-modules
WORKDIR /app
RUN git clone https://github.com/edenhill/librdkafka.git
WORKDIR /app/librdkafka
RUN /app/librdkafka/configure --prefix /usr
RUN make
RUN make install

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
# RUN sed -i 's/<PYPI_TOKEN>/${PYPI_TOKEN}/g' /requirements/base.txt

RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
