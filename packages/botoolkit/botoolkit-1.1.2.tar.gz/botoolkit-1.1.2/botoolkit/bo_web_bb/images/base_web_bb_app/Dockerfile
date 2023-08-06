FROM python:3.9.6
MAINTAINER Danilenko Alexander

ENV DJANGO_SETTINGS_MODULE=web_bb_app.settings
ENV DEBIAN_FRONTEND=noninteractive
ENV DOCKERIZE_VERSION v0.6.1

ARG TOOLKIT_GENERAL_RSA_PRIVATE_KEY
ARG WEB_BB_APP_BRANCH

# устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    git \
    openssh-client \
    grep \
    wget \
    python3-dev \
    libldap2-dev \
    libsasl2-dev \
    pkg-config \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    xmlsec1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv
RUN mkdir logs tmp configs

COPY ./app.conf.tmpl /srv/tmp
COPY ./app_requirements_ssh.txt.tmpl /srv/tmp

RUN mkdir -p /root/.ssh \
    && ssh-keyscan -t rsa -p 7999 -H stash.bars-open.ru >> /root/.ssh/known_hosts \
    && ssh-keyscan -t rsa -p 7999 -H 192.168.227.49 >> /root/.ssh/known_hosts \
    && echo "${TOOLKIT_GENERAL_RSA_PRIVATE_KEY}" | tr -d '\r' > ~/.ssh/id_rsa \
    && echo ~/.ssh/id_rsa \
    && chmod 700 ~/.ssh/id_rsa \
    && exec ssh-agent bash  \
    && ssh-add ~/.ssh/id_rsa

RUN cat ~/.ssh/id_rsa

RUN git clone ssh://git@stash.bars-open.ru:7999/budg/web_bb_app.git --branch ${WEB_BB_APP_BRANCH} --single-branch /srv/web_bb_app

COPY ./add_generic_tables.py /srv/web_bb_app/src/web_bb_app/management/commands
COPY ./create_default_date_range_partition.py /srv/web_bb_app/src/web_bb_app/management/commands

RUN pip3 install --no-cache-dir --no-binary="xmlsec" xmlsec
RUN pip3 install --no-cache-dir -r /srv/web_bb_app/requirements/stage.txt

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
