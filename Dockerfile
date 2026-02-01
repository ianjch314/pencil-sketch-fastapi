FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="$PATH:/home/appuser/.local/bin"

RUN mkdir /build
COPY requirements.txt /build

RUN mkdir /app
COPY ./app /app

ARG UID
ARG GID

RUN groupadd -g ${GID} appuser && \
    useradd -u ${UID} -g ${GID} -m -s /bin/bash appuser

RUN chown -R appuser:appuser /build
RUN chown -R appuser:appuser /app

USER appuser

WORKDIR /build
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

WORKDIR /app
CMD ["sleep", "infinity"]