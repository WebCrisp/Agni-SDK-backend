FROM python:3

ENV PYTHONUNBUFFERED=1

COPY . ./usr/src/app

WORKDIR /usr/src/app

# Install dependencies
RUN pip install -r requirements.txt
