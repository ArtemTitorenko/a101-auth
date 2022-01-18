FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app
ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"
RUN apk add --no-cache \
    curl `# для установки poetry` \
    git `# для установки зависимостей из git` \
    build-base  `# для сборки пакетов` \
    postgresql-dev `# для psycopg2` \
    libjpeg-turbo-dev zlib-dev libffi-dev cairo-dev libwebp-dev `# для pillow` \
    openssl-dev cargo `# для cryptography` \
    musl-locales musl-locales-lang `# для работы русской локали в python`
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN mkdir /app
COPY pyproject.toml /app/
WORKDIR /app/
ARG POETRY_PARAMS
RUN poetry install $POETRY_PARAMS
COPY wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for
COPY / /app/
RUN chmod 777 entrypoint.sh
RUN chmod 777 entrypoint.test.sh
