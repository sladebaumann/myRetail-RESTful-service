FROM python:2-alpine

MAINTAINER Slade Baumann

RUN pip install --no-cache-dir gunicorn

COPY /. /myretail-restful-service

RUN pip install -e /myretail-restful-service

EXPOSE 8080
CMD ["gunicorn", \
    "-b", "0.0.0.0:8080", \
    "myretail_restful_service.wsgi:app.api"\
    ]