FROM phusion/baseimage
MAINTAINER Chilles

RUN apt-get update && apt-get -y install vim python-psycopg2 \
    postgresql-server-dev-9.3 python-dev binutils libproj-dev gdal-bin curl \
    python-pip build-essential libssl-dev libffi-dev git

RUN mkdir /fundamentals
WORKDIR /fundamentals
COPY requirements.txt /fundamentals/
RUN pip install -r requirements.txt

RUN rm -f /etc/service/sshd/down
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN /usr/sbin/enable_insecure_key

RUN echo 'root:root' | chpasswd

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 22 8000