FROM python:3.10.0
LABEL Author=Pantilei

ENV PYTHONUNBUFFERED 1

RUN mkdir www

WORKDIR /www

COPY ./requirements.txt ./requirements.txt


RUN pip3 install --upgrade pip


RUN pip3 install -r ./requirements.txt

RUN mkdir app
COPY ./app ./app

COPY ./start_server.sh ./start_server.sh
RUN chmod u+x ./start_server.sh

ENTRYPOINT [ "./start_server.sh" ]


