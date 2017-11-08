FROM python:3
RUN apt-get update -y
RUN apt-get install -y python python-pip python-dev build-essential libpq-dev

ADD . /code
WORKDIR /code/app/yowsup

RUN python3 setup.py install

WORKDIR /code

RUN pip install --upgrade pip && pip install yowsup2 && pip install sqlalchemy && pip install coinmarketcap && pip install pandas
