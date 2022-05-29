FROM python:3.8.3-alpine
RUN apk --update add bash nano py3-requests

EXPOSE 9896
EXPOSE 9897
EXPOSE 9898
EXPOSE 9899

RUN pip3 install requests

COPY . /master
WORKDIR /master

ENTRYPOINT ["python","-u","master.py"]
