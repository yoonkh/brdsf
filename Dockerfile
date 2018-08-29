FROM python:3.6-stretch


WORKDIR /home/eb_docker
COPY requirements.txt ./requirements.txt
COPY boot.sh ./boot.sh
COPY application.py ./application.py
COPY app ./app
COPY config.py ./config.py
RUN pip3 install -U pip
RUN pip3 install -U setuptools
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

ENV FLASK_APP application.py
ENV FLASK_ENV production
ENV DB_HOST bstnt2.c0grph7n5f6y.ap-northeast-2.rds.amazonaws.com
ENV DB_NAME bstnt
ENV DB_USERNAME blackruby
ENV DB_PASSWORD blackruby!
ENV DB_NAME bstnt

EXPOSE 8000
RUN chmod +x ./boot.sh
ENTRYPOINT ["./boot.sh"]