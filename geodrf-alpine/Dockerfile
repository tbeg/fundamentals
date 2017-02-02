# This image provides containers that can connect to a postGIS database instance.
FROM python:2.7-alpine
ENV CFLAGS="$CFLAGS -L/lib"
ENV PYTHONUNBUFFERED 0
RUN apk add --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
    bash \
    binutils \
    gcc \
    gdal \
    geos \
    git \
    jpeg-dev \
    libffi-dev \
    vim \
    libpq \
    linux-headers \
    mailcap \
    musl-dev \
    proj4-dev \
    postgresql \
    postgresql-client \
    postgresql-dev \
    libxml2-dev \
    libxslt-dev \
    zlib-dev && \
    rm -rf /var/cache/apk/*
RUN ln -s /usr/lib/libgeos_c.so.1 /usr/local/lib/libgeos_c.so
RUN ln -s /usr/lib/libgdal.so.20.1.0 /usr/local/lib/libgdal.so
RUN pip install --upgrade pip
