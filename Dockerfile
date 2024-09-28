FROM python:3.11-alpine

WORKDIR usr/src/app

COPY ./nebula ./nebula
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install waitress

EXPOSE 8888

CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8888", "--call", "nebula:create_app"]