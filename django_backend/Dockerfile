FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "/usr/src/app/django_backend/entrypoint.sh" ]






