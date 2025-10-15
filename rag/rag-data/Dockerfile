FROM postgres:18.0-alpine AS build

WORKDIR /var/lib/postgresql/

COPY ./config.sh /docker-entrypoint-initdb.d/

USER root
RUN chown -R postgres:postgres /var/lib/postgresql/ /docker-entrypoint-initdb.d/ && \
    chmod -R 0700 /var/lib/postgresql/ /docker-entrypoint-initdb.d/

USER postgres

EXPOSE 5432