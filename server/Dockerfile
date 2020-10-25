FROM python:3.8-buster
RUN apt-get update && apt-get install -y sqlcipher libsqlcipher-dev libpython3-dev libsqlite3-dev

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY . /telehelp/server
WORKDIR /telehelp/server

EXPOSE 5000
