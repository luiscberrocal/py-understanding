FROM python:3.10.10-bullseye

ENV PYTHONUNBUFFERED 1

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

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN chown -R django:django /app
RUN chmod -R 755 /app

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements

RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=django:django ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --chown=django:django ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


COPY --chown=django:django ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY --chown=django:django . /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
