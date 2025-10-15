#!/bin/bash

# allow pgadmin-dev to connect to the server
PGADMIN_IP=$(getent hosts rag-pgadmin | awk '{ print $1 }')
echo "host    all             all             ${PGADMIN_IP}/32           trust" >> /var/lib/postgresql/data/pg_hba.conf

# allow backend-dev to connect to the server
RAG_IP=$(getent hosts rag-service | awk '{ print $1 }')
echo "host    all             all             ${RAG_IP}/32           trust" >> /var/lib/postgresql/data/pg_hba.conf