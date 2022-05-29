FROM python:3.8.3-alpine
RUN apk --update add bash nano

COPY . /node
WORKDIR /node

ENTRYPOINT ["python", "-u", "node.py"]