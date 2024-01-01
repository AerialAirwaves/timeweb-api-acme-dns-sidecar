ARG PYTHON_VERSION=3.12
ARG BASE_DISTRO=slim-bookworm

FROM python:${PYTHON_VERSION}-${BASE_DISTRO}
ENV ENV_POETRY_VERSION 1.7.1
ENV ENV_DEPENDENCIES_PACKAGES "gcc libc6-dev"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN python -m pip install --no-cache-dir poetry==$ENV_POETRY_VERSION \
    && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN apt-get update \
    && apt-get install -y --no-install-recommends $ENV_DEPENDENCIES_PACKAGES \
    \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts} \
    \
    && apt-get purge -y $ENV_DEPENDENCIES_PACKAGES \
    && apt-get autoremove -y \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

COPY ./src/ /app/

CMD ["python", "main.py"]
