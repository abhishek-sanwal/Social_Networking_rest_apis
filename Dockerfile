FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1

WORKDIR /project
COPY  requirements.txt /project/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

