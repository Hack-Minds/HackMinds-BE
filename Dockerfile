FROM python:latest

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get install --auto-remove -y \
      binutils \
      libproj-dev \
      gdal-bin \
      postgis && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py","runserver", "0.0.0.0:8000"]