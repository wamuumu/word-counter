FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano

ENV STATIC_URL /static
ENV STATIC_PATH /monitor/app/static

COPY ./requirements.txt /monitor/requirements.txt
RUN pip install -r /monitor/requirements.txt

WORKDIR /monitor/