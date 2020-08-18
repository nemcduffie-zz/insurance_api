FROM ubuntu:16.04

MAINTAINER Nicole McDuffie "nicole.mcduffie@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --upgrade pip

COPY . /insurance_api

WORKDIR /insurance_api

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3.8" ]

CMD [ "run.py" ]
