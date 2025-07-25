FROM python:3.12 AS builder

ARG SQLALCHEMY_DATABASE_URI
ENV SQLALCHEMY_DATABASE_URI=$SQLALCHEMY_DATABASE_URI

WORKDIR /code

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==1.4.2

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY ./ /code

CMD ["gunicorn", "manage:app", "-b", "0.0.0.0:5000", "--workers", "4"]