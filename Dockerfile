# Creating a python base with shared environment variables
FROM python:3.11-slim-bullseye AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_HOME="/opt/uv" \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$UV_HOME/bin:$VENV_PATH/bin:$PATH"

# builder-base is used to build dependencies
FROM python-base AS builder-base
RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    vim \
    netcat \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# We copy our Python requirements here to cache them
# and install only runtime deps using uv
WORKDIR $PYSETUP_PATH
COPY ./requirements.txt ./
RUN uv venv $VENV_PATH && \
    . $VENV_PATH/bin/activate && \
    uv pip install -r requirements.txt

# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /app
FROM python-base as development
ENV FASTAPI_ENV=development

# Copying uv and venv into image
COPY --from=builder-base $UV_HOME $UV_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Copying in our entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# venv already has runtime deps installed we get a quicker install
WORKDIR $PYSETUP_PATH
COPY ./dev-requirements.txt ./
RUN . $VENV_PATH/bin/activate && \
    uv pip install -r dev-requirements.txt

WORKDIR /app
COPY . .

# Needs to be consistent with gunicorn_conf.py
EXPOSE 8000
ENTRYPOINT ["/docker-entrypoint.sh"]

# 'production' stage uses the clean 'python-base' stage and copies
# in only our runtime deps that were installed in the 'builder-base'
FROM python-base AS production
ENV FASTAPI_ENV=production
ENV PROD=true

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY gunicorn_conf.py /gunicorn_conf.py

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY main.py /main.py
COPY .env /.env

# Create user with the name appuser
RUN groupadd -g 1500 appuser && \
    useradd -m -u 1500 -g appuser appuser

COPY --chown=appuser:appuser ./app /app
USER appuser

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--config", "/gunicorn_conf.py", "main:server"]
