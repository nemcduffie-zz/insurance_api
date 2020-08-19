#!/bin/bash

pip install --upgrade pip
pip install -r requirements.txt --no-use-pep517

psql postgresql://postgres:postgres@localhost -c "drop database insurance_api;"
psql postgresql://postgres:postgres@localhost -c "create database insurance_api with 
    OWNER = postgres
    ENCODING = 'UTF8';"
psql postgresql://postgres:postgres@localhost -c "drop database insurance_api;"
psql postgresql://postgres:postgres@localhost -c "create database insurance_api with 
    OWNER = postgres
    ENCODING = 'UTF8';"


FLASK_APP=run.py flask db upgrade
export FLASK_APP=run.py
