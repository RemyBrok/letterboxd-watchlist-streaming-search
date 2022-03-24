# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY docker/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm requirements.txt

COPY ./online .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]