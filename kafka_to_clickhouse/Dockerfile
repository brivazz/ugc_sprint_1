FROM python:3.11-slim-buster

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/opt

RUN mkdir -p /opt/src

COPY ../requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY src src/.

CMD ["python", "src/main.py"]
