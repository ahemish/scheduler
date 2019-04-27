FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /DashBoardApp
WORKDIR /DashBoardApp
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["__init__.py"]

# FROM alpine:latest

# RUN apk add python3 && apk add py-pip && pip install -r requirements.txt && apk add nginx && apk add supervisor