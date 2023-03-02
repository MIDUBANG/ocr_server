FROM python:3.8.0

WORKDIR /app
#WORKDIR /usr/src/app

ADD . /app
# ADD . /usr/src/app
RUN pip install -r requirements.txt

CMD ["uwsgi","uwsgi.ini"]