FROM python:3.10-alpine

# ENVS
ENV PYTHONUNBUFFERED=1

WORKDIR app

# Install system requirements
RUN apk add --update --no-cache --virtual .tmp \
    python3-dev build-base linux-headers pcre-dev \
    jpeg-dev zlib-dev \        
    postgresql-dev

RUN apk add --no-cache --update libpq bash

# Install python requirements
COPY Pipfile* .

RUN pip install --no-cache-dir pipenv
RUN pipenv install --system

# Clear caches and temps
RUN pipenv --clear \
    && apk del .tmp \
    && adduser -D fastapi 

# Copy source code
COPY ./src /app/src

# Run application
EXPOSE 80

USER fastapi

CMD ["python3", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]