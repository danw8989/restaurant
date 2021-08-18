
FROM python:3.9

RUN mkdir /app
WORKDIR /app

ADD . /app/

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

ENV PORT=8000
ENV DEBUG=1
ENV TZ=Europe/Warsaw

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        wait-for-it \
        cron
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* 

# configure and apply cron
COPY mail-cron /etc/cron.d/mail-cron
RUN chmod 0644 /etc/cron.d/mail-cron
RUN crontab /etc/cron.d/mail-cron
RUN touch /var/log/cron.log
RUN cron

# install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

# Install project dependencies
RUN pipenv install --skip-lock --system --dev

EXPOSE $PORT
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]