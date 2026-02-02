# Base image
FROM python:3.14-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# Developement stage
FROM base as development

ARG UID
ARG GID

RUN groupadd -g ${GID} devuser && \
    useradd -u ${UID} -g devuser -m devuser && \
    chown -R devuser:devuser /app

USER devuser
COPY --chown=devuser:devuser ./app .
CMD ["fastapi", "run", "main.py", "--port", "8000", "--reload"]

# Production stage
FROM base as production

RUN groupadd -r appuser && \
    useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app

USER appuser
COPY --chown=appuser:appuser ./app .
CMD ["fastapi", "run", "main.py", "--port", "8000"]
