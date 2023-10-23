FROM python:3.10

RUN apt update

ENV PYTHONPATH=/app/src

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r Docker/development/requirements.txt
RUN pipenv install --deploy --system --ignore-pipfile
EXPOSE 8000