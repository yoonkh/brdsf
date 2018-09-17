FROM python:3.6-stretch

RUN useradd brandsaferapi

WORKDIR /home/brandsaferapi

RUN pip3 install -U pip
RUN pip3 install -U setuptools
RUN pip3 install gunicorn


COPY boot.sh boot.sh
COPY application.py application.py
COPY app app
COPY config.py config.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt


EXPOSE 8000
RUN chmod a+x boot.sh
ENTRYPOINT ["./boot.sh"]